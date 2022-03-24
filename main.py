import csv
import os
from shortest_url_handler import Shortest_Url_Handler
import xlwt
from dao import mysql

if __name__ == '__main__':
    database = mysql()
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('data')
    ro = -1
    co = 0
    check_exist_by_app_name_sql = "select * from desensitization_result where app_name='{}'"
    delete_by_app_name_sql = "delete from desensitization_result where app_name='{}'"
    insert_sql = "insert into desensitization_result(app_name, mes, ori_url, url, similarity) values('{}', '{}', '{}', '{}', {})"
    with open('files/ori_data.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cur = ''
        for row in reader:
            try:
                if len(row[2]) != 0:
                    ro += 1
                    co = 0
                    cur_app_name = row[2]
                    print(cur_app_name)
                    # worksheet.write(ro, co, cur_app_name)
                    if database.is_exit(check_exist_by_app_name_sql.format(cur_app_name)):
                        # 之前跑过不重跑！
                        continue
                    # database.query(delete_by_app_name_sql.format(cur_app_name))
                    co += 1
                items = [row[7], row[10], row[13]]
                insert_new_data = False
                for item in items:
                    l = item.find('http://')
                    if l == -1:
                        l = item.find('https://')
                    if l == -1:
                        continue
                    r = l
                    while r < len(item) and item[r] != ' ' and item[r] != '\n':
                        r += 1
                    ori_url = item[l:r]
                    suh = Shortest_Url_Handler(ori_url)
                    mes, url, similarity = suh.get_shortest_url()
                    database.query(insert_sql.format(cur_app_name, mes, ori_url, url, similarity))
                    insert_new_data = True
                    output = '{}: {} -> {:.2f}%'.format(mes, url, similarity * 100)
                    print(output)
                    # worksheet.write(ro, co, output)
                    co += 1
                    # suh.close()
                if not insert_new_data:
                    database.query(insert_sql.format(cur_app_name, '无url记录', '', '', 0.0))
            except Exception as e:
                print(e)
        # workbook.save('data.xlsx')