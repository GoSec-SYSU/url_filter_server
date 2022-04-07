# 用于转化单个参数
from typing import List
import os


def trans_standard_to_smail_form(str: str) -> str:
    # if 方法名是构造方法，则  <init> -> $init
    # if 类型不是数组类型： 直接返回
    # else 基本类型：[特殊标志
    #      类类型：[L类名;
    str = ''.join(str.split())
    # 构造函数，直接转换并返回
    if str == '<init>':
        return '$init'
    if '[' not in str:
        return str
    # 左括号的数量
    left_bracket_num = 0
    # 数左括号的数量
    for c in str:
        if c == '[':
            left_bracket_num += 1
    # 清除所有左右括号
    str = str.replace('[', '')
    str = str.replace(']', '')
    # 类类型
    if '.' in str:
        str = 'L' + str + ';'
    # 基本类型
    else:
        tran_dic = {
            'boolean': 'Z',
            'byte': 'B',
            'char': 'C',
            'double': 'D',
            'float': 'F',
            'int': 'I',
            'long': 'J',
            'short': 'S',
        }
        for key, val in tran_dic.items():
            if key in str:
                str = str.replace(key, val)
    # 添加左括号到左边
    for time in range(left_bracket_num):
        str = '[' + str
    return str


# 处理全部
def transform(str: str):
    str = ''.join(str.split())
    # 返回值类型，有(开头
    if '(' in str:
        arr = []
        arr = str[1:len(str) - 1].split(',')
        for i in range(len(arr)):
            arr[i] = trans_standard_to_smail_form(arr[i])
        return arr
        # str = ','.join(arr)
        # str = '(' + str + ')'
    else:
        str = trans_standard_to_smail_form(str)
    return str


# 读取sink文件
def handle_sink(sink_data: str) -> dict:
    d = dict()
    if sink_data != '' and sink_data[0] == '<':
        items = sink_data.split()
        # <okhttp3.Request: okhttp3.Request.Builder url(java.lang.String)> -> _SINK_
        d['targetClass'] = transform(items[0][1:len(items[0]) - 1])
        left_bracket_index = 0
        # print('str: ', sink_data)
        while items[2][left_bracket_index] != '(':
            left_bracket_index += 1
        d['targetReturn'] = transform(items[1])
        d['targetMethod'] = transform(items[2][0:left_bracket_index])
        d['targetArguments'] = transform(
            items[2][left_bracket_index:len(items[2]) - 1])
    return d


def read(url: str):
    sink_dict = dict()
    method_dict = dict()
    cur_package_name = ''
    with open(url, encoding='utf-8') as f:
        line = f.readline()
        while line:
            try:
                if line.startswith('app:'):
                    if cur_package_name != '':
                        sink_dict[cur_package_name] = method_dict
                    cur_package_name = line.split(':')[1].strip()
                    method_dict = dict()
                elif line.startswith('<') and cur_package_name != '':
                    data = handle_sink(line)
                    if data['targetClass'] not in method_dict:
                        method_dict[data['targetClass']] = dict()
                    if data['targetMethod'] not in method_dict[data['targetClass']]:
                        method_dict[data['targetClass']][data['targetMethod']] = []
                    method_dict[data['targetClass']][data['targetMethod']].append(data['targetArguments'])
            except Exception as e:
                pass
            finally:
                line = f.readline()
    if cur_package_name != '':
        sink_dict[cur_package_name] = method_dict
    return sink_dict


if __name__ == '__main__':
    data = read(os.path.join(os.path.dirname(__file__), 'files', 'base_sink.txt'))
    print(data)
