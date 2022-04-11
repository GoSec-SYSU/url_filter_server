import os
import time
from selenium import webdriver
import requests
import lxml
import re
from code_similarity import CosineSimilarity

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
    # options.add_argument("--headless")  # 设置火狐为headless无界面模式
    options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(executable_path=path, options=options)
    # browser.maximize_window()
    browser.set_window_size(1280, 800)
    # url = 'https://w8.soulsmile.cn/activity/#/web/user?targetUserIdEcpt=NVhKUEpCaEFHbkZYRnBhV05La1orUT09&userIdEcpt=NVhKUEpCaEFHbkZYRnBhV05La1orUT09&shareUserId=aGlEbXFkMno5M3FodUl5MEpNOUVkQT09&titleNum=4&sec=yLkHkMErPVtu06KD9925BTpWQhMT37ka'
    url = 'https://www.xiaohongshu.com/discovery/item/624233900000000001027fca?share_from_user_hidden=2du40DfRyZIPGQq1mUeXtrue&xhsshare=lKqNyjh5W9bncZmXTGpdWeixinSession&appuid=FsBiYqglAPoXkctOpD345a07b18711be103e932d89dd&apptime=V6akghYCo03tjJEu7f2q1648524076'
    short_str = sel_get(url, 'files/short.jpg')
    print(short_str)
    # write(os.path.join(os.getcwd(), 'tmp', 'sel_short.html'), short_str)
    # print('--------------------------')
    #
    # url = 'https://w8.soulsmile.cn/activity/#/web/user'
    # # url = 'https://w8.soulsmile.cn/activity/#/web/user?targetUserIdEcpt=NVhKUEpCaEFHbkZYRnBhV05La1orUT09&userIdEcpt=NVhKUEpCaEFHbkZYRnBhV05La1orUT09&shareUserId=aGlEbXFkMno5M3FodUl5MEpNOUVkQT09&titleNum=4&sec=yLkHkMErPVtu06KD9925BTpWQhMT37ka'
    #
    # ori_str = sel_get(url, 'files/ori.jpg')
    # print(ori_str)
    # write(os.path.join(os.getcwd(), 'tmp', 'sel_ori.html'), ori_str)
    # print('--------------------------')

    # similarity = CosineSimilarity(short_str, ori_str)
    # similarity = similarity.main()
    # print('相似度: %.2f%%' % (similarity * 100))
