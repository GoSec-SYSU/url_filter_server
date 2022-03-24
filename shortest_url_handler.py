import re
import os
import time

from selenium import webdriver
from code_similarity import CosineSimilarity
import cv_similarity
import redis
from single.yaml_reader import Yaml_Reader
from single.brower import Browser_Getter


class Shortest_Url_Handler:
    def __init__(self, url, code_threshold=0.90, cv_threshold=0.75, maximum_search_time=2 ** 10):
        browser_getter = Browser_Getter()
        self.browser = browser_getter.get_brower()
        self.url = url
        arr = re.split('\?|&', url)
        self.domain = arr[0]
        self.arguments = arr[1:]
        self.screenshot_path = os.path.join(os.getcwd(), 'screenshot',
                                            self.domain.replace('/', '.').replace(':', '.').replace('?', '.'))
        # self.screenshot_path = os.path.join(os.getcwd(), 'screenshot', 'hahahah')
        if not os.path.exists(self.screenshot_path):
            os.makedirs(self.screenshot_path)
        self.cv_threshold = cv_threshold
        self.code_threshold = code_threshold
        self.header = {'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
        self.maximum_code_similarity = -1
        self.maximum_code_similarity_url = url
        self.maximum_cv_similarity = -1
        self.maximum_cv_similarity_url = url
        self.ori_url_screenshot_path = os.path.join(self.screenshot_path, 'ori_url_screenshot.png')
        self.ori_url_title, self.ori_url_content = self.get_url_title_and_content(url)
        self.save_url_screenshot(url, self.ori_url_screenshot_path)
        self.search_time = 0
        self.maximum_search_time = maximum_search_time
        self.redis_key = self.get_redis_key(self.domain, self.arguments)
        # redis连接
        yaml_reader = Yaml_Reader()
        data = yaml_reader.get_data()
        self.r = redis.StrictRedis(host=data['redis_confi']['host'], port=data['redis_confi']['port'],
                                   db=data['redis_confi']['db'], decode_responses=True)
        print('self.redis_key: ', self.redis_key)
        self.tmp = []

    # domain: https://www.baidu.com
    # arguments: ['name=xinxin', 'age=22', 'gender=male']
    def get_redis_key(self, domain: str, arguments: []) -> str:
        ans = domain
        n = len(arguments)
        for i in range(n):
            if i == 0:
                ans += '?'
            equal_index = arguments[i].find('=')
            if equal_index == -1:
                ans += arguments[i]
            else:
                arge = arguments[i][:equal_index]
                ans += arge
            if i != n - 1:
                ans += '&'
        return ans

    def close(self):
        self.browser.close()

    def get_can(self):
        return len(self.arguments)

    def get_cur_url(self):
        ans = self.domain
        if len(self.tmp) != 0:
            ans += '?' + '&'.join(self.tmp)
        return ans

    def get_url_title_and_content(self, url):
        self.browser.get(url)
        time.sleep(1)
        pageSource = self.browser.page_source
        title = self.browser.title
        return title, pageSource

    def save_url_screenshot(self, url, img_path):
        self.browser.get(url)
        time.sleep(2)
        self.browser.save_screenshot(img_path)

    def check(self):
        self.search_time += 1
        if self.search_time > self.maximum_search_time:
            return True
        # cv检测
        cur_url = self.get_cur_url()
        cur_url_screenshot_path = os.path.join(self.screenshot_path,
                                               cur_url.replace('/', '.').replace(':', '.').replace('?', '.') + '.png')
        self.save_url_screenshot(cur_url, cur_url_screenshot_path)
        cur_cv_similarity = cv_similarity.classify_hist_with_split_by_img_path(self.ori_url_screenshot_path,
                                                                               cur_url_screenshot_path)
        print('cv: ', cur_url, ' -> ', '相似度: %.2f%%' % (cur_cv_similarity * 100))
        # cv最大，cv说可以就是可以！
        if self.cv_threshold < cur_cv_similarity:
            self.maximum_cv_similarity = cur_cv_similarity
            self.maximum_cv_similarity_url = cur_url
            return True

        # 源代码相似性+title检测
        cur_url_title, cur_url_content = self.get_url_title_and_content(cur_url)
        code_similarity = CosineSimilarity(self.ori_url_content, cur_url_content)
        code_similarity = code_similarity.main()
        print('code: ', cur_url, ' -> ',
              '原始title: %s, 当前title: %s, 相似度: %.2f%%' % (self.ori_url_title, cur_url_title, code_similarity * 100))
        if cur_url_title == self.ori_url_title and self.maximum_code_similarity < code_similarity:
            self.maximum_code_similarity_url = cur_url
            self.maximum_code_similarity = code_similarity
        # 达到我们的阈值，直接结束
        if cur_url_title == self.ori_url_title and code_similarity >= self.code_threshold:
            return True
        return False

    def get_filted_url_by_redis(self) -> (bool, str):
        if not self.r.exists(self.redis_key):
            return False, ""
        argus_in_redis = set(self.r.get(self.redis_key).split('&'))
        # self.redis_key = https://baidu.com?name&age&gender
        # self.arguments = ['name=xinxin', 'age=22', 'gender=male']
        arges_mp = {}
        for argu_raw in self.arguments:
            equal_index = argu_raw.find('=')
            if equal_index == -1:
                arges_mp[argu_raw] = argu_raw
            else:
                arges_mp[argu_raw[:equal_index]] = argu_raw
        arges_redis_mp = set(str(self.r[self.redis_key]).split('&'))
        ans = self.domain
        first = True
        for (argu, val) in arges_mp.items():
            if argu in arges_redis_mp:
                if first:
                    first = False
                    ans += '?'
                else:
                    ans += '&'
                ans += val
        return True, ans

    def set_redis(self, redis_key: str, filted_url: str):
        arr = re.split('\?|&', filted_url)
        val_arr = []
        if len(arr) > 1:
            for i in range(1, len(arr)):
                argu_raw = arr[i]
                equal_index = argu_raw.find('=')
                if equal_index == -1:
                    val_arr.append(argu_raw)
                else:
                    val_arr.append(argu_raw[:equal_index])
        val = '&'.join(val_arr)
        self.r.set(redis_key, val)

    def get_shortest_url(self):
        # 之前有过直接处理返回
        flag, ans = self.get_filted_url_by_redis()
        if flag:
            print('之前有过了，直接返回')
            return '之前有过了，直接返回', ans, 1.0
        get_shortest = False
        for i in range(2):
            for length in range(len(self.arguments) + 1):
                if self._get_shortest_url(0, length):
                    get_shortest = True
                    break
            if get_shortest:
                break
        res_mes = ''
        res_url = ''
        res_similarity = 1.0
        if self.search_time > self.maximum_search_time:
            res_mes = "达到最大上限，返回原始url"
            res_url = self.url
            res_similarity = 1.0
        elif self.maximum_cv_similarity >= self.cv_threshold:
            res_mes = "cv脱敏成功"
            res_url = self.maximum_cv_similarity_url
            res_similarity = self.maximum_cv_similarity
        elif self.maximum_code_similarity >= self.code_threshold:
            res_mes = "code脱敏成功"
            res_url = self.maximum_code_similarity_url
            res_similarity = self.maximum_code_similarity
        else:
            res_mes = "脱敏失败，返回原url"
            res_url = self.url
            res_similarity = 1.0
        self.set_redis(self.redis_key, self.url)
        return res_mes, res_url, res_similarity

    def _get_shortest_url(self, i, length):
        if length == 0:
            return self.check()
        if i >= len(self.arguments):
            return
        for j in range(i, len(self.arguments)):
            self.tmp.append(self.arguments[j])
            if self._get_shortest_url(j + 1, length - 1):
                return True
            self.tmp.pop()
        return False


if __name__ == '__main__':
    with open('./files/url.txt', 'r', encoding='utf-8') as f:
        url = f.read()
        print(url)
        suh = Shortest_Url_Handler(url)
        print(suh.get_shortest_url())
        # arr = re.split('\?|&', url)
        # print(arr)
