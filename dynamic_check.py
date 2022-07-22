import functools
import os
import random
import shutil
import string

import commands

from dao import mysql

import androguard.core.bytecodes.apk as ak

import csv
import os
from shortest_url_handler_replace import Shortest_Url_Handler_Replace
import xlwt
from dao import mysql

if __name__ == '__main__':
    # database = mysql()
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('data')
    ro = -1
    co = 0
    check_exist_by_app_name_sql = "select * from desensitization_replace_result where app_name='{}'"
    delete_by_app_name_sql = "delete from desensitization_replace_result where app_name='{}'"
    insert_sql = "insert into desensitization_replace_result(app_name, mes, ori_url, url, similarity) values('{}', '{}', '{}', '{}', {})"
    hang = 0
    with open('files/ori_data.csv', 'r', encoding='utf-8') as csvfile:
        arr = set()
        reader = csv.reader(csvfile)
        for row in reader:
            arr.add(row[0])
        print(arr)
        print(len(arr))

        not_exit = set()
        g = os.walk('H:/跑实验/300app_china_new')
        for path, dir_list, file_list in g:
            for file_name in file_list:
                l, r, n = 0, len(file_name) - 1, len(file_name)
                while r >= 0 and file_name[r] != '.':
                    r -= 1
                target = file_name[:r]
                if target not in arr:
                    print('不存在：', file_name)
                    not_exit.add(target)

        print("共：", len(not_exit))

        os.asdsa()
        reader = csv.reader(csvfile)
        cur = ''
        for row in reader:
            try:
                for i in range(min(len(row), 4)):
                    output = ''
                    str = row[i]
                    if str == '':
                        worksheet.write(hang, i, label='无')
                    elif str.find('https') == -1 and str.find('http') == -1:
                        output = str
                        worksheet.write(hang, i, label=str)
                    elif str.find('https') != -1 or str.find('http') != -1:
                        print(str)
                        print('-------------------------')
                        l, r, n = 0, 0, len(str)
                        # print(row[i])
                        # print('________________________')
                        while r < n:
                            while l < n and (str[l] == ' ' or str[l] == '\n'):
                                l += 1
                            r = l
                            while r < n and str[r] != '\n':
                                r += 1
                            output += str[l:r] + '\n'
                            output += str[l:r] + '\n'
                            # print(str[i][l:r])
                            r += 1
                            l = r
                        print(output)
                        worksheet.write(hang, i, label=(output))
            except Exception as e:
                print('error: ', e)
            hang += 1
        workbook.save('res.xlsx')
