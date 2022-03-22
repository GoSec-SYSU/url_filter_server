import re
import os
import time

from selenium import webdriver
from same import CosineSimilarity
import cv_check


class Shortest_Url_Handler:
    def __init__(self, url, code_threshold=0.90, cv_threshold=0.50, maximum_search_time=2 ** 10):
        path = os.path.join(os.getcwd(), 'browser', 'chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 设置火狐为headless无界面模式
        options.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome(executable_path=path, options=options)
        self.url = url
        arr = re.split('\?|&', url)
        self.domain = arr[0]
        self.screenshot_path = os.path.join(os.getcwd(), 'screenshot', self.domain.replace('/', '.').replace(':', '.').replace('?', '.'))
        # self.screenshot_path = os.path.join(os.getcwd(), 'screenshot', 'hahahah')
        if not os.path.exists(self.screenshot_path):
            os.makedirs(self.screenshot_path)
        self.cv_threshold = cv_threshold
        self.code_threshold = code_threshold
        self.arguments = arr[1:]
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
        self.tmp = []

    def get_can(self):
        return len(self.arguments)

    def get_cur_url(self):
        ans = self.domain
        if len(self.tmp) != 0:
            ans += '?' + '&'.join(self.tmp)
        return ans

    def get_url_title_and_content(self, url):
        self.browser.get(url)
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
        cur_cv_similarity = cv_check.classify_hist_with_split_by_img_path(self.ori_url_screenshot_path, cur_url_screenshot_path)
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
        print('code: ', cur_url, ' -> ', '当前title: %s, 相似度: %.2f%%' % (cur_url_title, code_similarity * 100))
        if cur_url_title==self.ori_url_title and self.maximum_code_similarity < code_similarity:
            self.maximum_code_similarity_url = cur_url
            self.maximum_code_similarity = code_similarity
        # 达到我们的阈值，直接结束
        if code_similarity >= self.code_threshold:
            return True
        return False

    def get_shortest_url(self):
        get_shortest = False
        for i in range(2):
            for length in range(len(self.arguments) + 1):
                if self._get_shortest_url(0, length):
                    get_shortest = True
                    break
            if get_shortest:
                break
        if self.search_time > self.maximum_search_time:
            return "达到最大上限，返回原始url", self.url, 1.0
        if self.maximum_cv_similarity >= self.cv_threshold:
            return "cv脱敏成功", self.maximum_cv_similarity_url, self.maximum_cv_similarity
        if self.maximum_code_similarity >= self.code_threshold:
            return "code脱敏成功", self.maximum_code_similarity_url, self.maximum_code_similarity
        return "脱敏失败，返回原始", self.url, 1.0

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
