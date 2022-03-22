import os
import time
from selenium import webdriver
import requests
import lxml
import re
from same import CosineSimilarity

def sel_get(url, img_file):
    browser.get(url)
    pageSource = browser.page_source
    time.sleep(1)
    browser.save_screenshot(img_file)
    print('browser.title: ', browser.title)
    return pageSource


def get_url_content(url):
    header = {'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
    respon = requests.get(url, headers=header)
    data = respon.text
    return data


def write(file, content):
    # 打开一个文件
    fo = open(file, "w", encoding='utf-8')
    fo.write(content)
    # 关闭打开的文件
    fo.close()


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'browser', 'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 设置火狐为headless无界面模式
    options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(executable_path=path, options=options)
    url = 'https://www.iqiyi.com/v_1pkjkyp9rvk.html'
    short_str = sel_get(url, 'files/short.jpg')
    print(short_str)
    write(os.path.join(os.getcwd(), 'tmp', 'sel_short.html'), short_str)
    print('--------------------------')
    url = 'http://m.iqiyi.com/v_1pkjkyp9rvk.html?key=456ddd1ff52a6089c7e3f806d609520d&msrc=3_31_56&aid=8136869546987501&tvid=6265416625426700&cid=2&identifier=weixinv1&ftype=27&subtype=1&vip_pc=0&vip_tpc=1&isrd=1&p1=2_22_222&social_platform=link&_psc=9cbebf3693354fc0a7be79366b18ff3f'
    ori_str = sel_get(url, 'files/ori.jpg')
    print(ori_str)
    write(os.path.join(os.getcwd(), 'tmp', 'sel_ori.html'), ori_str)
    print('--------------------------')

    similarity = CosineSimilarity(short_str, ori_str)
    similarity = similarity.main()
    print('相似度: %.2f%%' % (similarity * 100))
