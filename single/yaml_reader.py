import yaml, os
import redis


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner

@singleton
class Yaml_Reader(object,):
    def __init__(self):
        # 获取文件全路径
        filename = os.path.join(os.path.dirname(__file__), '..', 'config', 'confi.yaml').replace("\\", "/")
        file = open(filename, 'r', encoding='utf-8')
        file_data = file.read()
        self.data = yaml.load(file_data, Loader=yaml.FullLoader)

    def get_data(self):
        return self.data

if __name__ == '__main__':
    yaml_reader = Yaml_Reader()
    print(yaml_reader.get_data())