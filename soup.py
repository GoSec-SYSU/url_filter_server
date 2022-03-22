from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    url = 'https://m.miguvideo.com/mgs/msite/prd/detail.html?channelid=201600010010022&sharefrom=miguvideoapp&cid=725681219&pwId=81aa6240f0f64409a22199dafaed892a'
    resp = requests.get(url=url)
    print(resp.status_code)
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
    try:
        for i in range(50):
            print(soup.find_all('p')[i].string)
    except:
        pass