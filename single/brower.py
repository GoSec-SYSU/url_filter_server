import yaml, os
import redis
from selenium import webdriver


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner

@singleton
class Browser_Getter(object,):
    def __init__(self):
        path = os.path.join(os.getcwd(), 'browser', 'chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 设置火狐为headless无界面模式
        options.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome(executable_path=path, options=options)

    def get_brower(self):
        return self.browser

if __name__ == '__main__':
    yaml_reader = Yaml_Reader()
    print(yaml_reader.get_data())