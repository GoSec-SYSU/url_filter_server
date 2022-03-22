import time
import requests
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

timesleep = 1
maxtime = 1
url = "https://www.bilibili.com/video/BV1Su411Q7a5"
headers = {'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}
a = requests.get(url, headers=headers).text
time.sleep(timesleep)
count = 0
print(a)
# while (count < maxtime):
#     b = requests.get(url, headers=headers).text
#     print(a)
#     print("Got it")
#     if (a != b):
#         a = b
#         msg = MIMEText(b.text, 'html', 'utf-8')
#         print("Sending mail...")
#         sendmail(msg)
#         count = count + 1
#     time.sleep(timesleep)
