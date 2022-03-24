import yaml, os
import redis
from single.yaml_reader import Yaml_Reader

if __name__ == '__main__':
    yaml_reader = Yaml_Reader()
    data = yaml_reader.get_data()
    r = redis.StrictRedis(host=data['redis_confi']['host'], port=data['redis_confi']['port'],
                          db=data['redis_confi']['db'], decode_responses=True)
    print(r['foo'])
