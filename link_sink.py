import csv
import os
from shortest_url_handler_replace import Shortest_Url_Handler_Replace
import xlwt
from dao import mysql
import re
import androguard.core.bytecodes.apk as ak


def have_content(arr: list) -> bool:
    if len(arr) <= 1:
        return False
    # 看看后面还有没有内容，如果有说明真的在泄露，否则就不认为有泄露，以免引入假阳性
    for i in range(1, len(arr)):
        if arr[i] != '':
            return True
    return False


def check_IMEI(arr: list) -> bool:
    # 一般只会在key中标识
    if len(arr) > 0 and arr[0].find('imei') != -1 and have_content(arr):
        return True
    return False


def check_ueser_logo(arr: list) -> bool:
    # 一般只会在key中标识
    sensitive_keys = ['userid', 'user_id', 'username', 'user_name', 'uid', 'uuid']
    if len(arr) > 0:
        for sensitive_key in sensitive_keys:
            if arr[0].find(sensitive_key) != -1 and have_content(arr):
                return True
    return False


def check_share_device(arr: list) -> list:
    # 一般只会在key中标识
    sensitive_keys = ['android', 'ios', 'window', 'mac']
    ans = []
    for item in arr:
        for sensitive_key in sensitive_keys:
            if item.find(sensitive_key) != -1:
                ans.append(sensitive_key)
    return ans


def check_share_platform(arr: list) -> list:
    # 一般只会在key中标识
    sensitive_keys = ['weixin', 'weibo', 'qq', 'moment', 'facebook', 'twitter']
    ans = []
    for item in arr:
        for sensitive_key in sensitive_keys:
            if item.find(sensitive_key) != -1:
                ans.append(sensitive_key)
    return ans


def get_key_val(url: str):
    arr = []
    ans = []
    if len(url.split('?')) == 1:
        return arr
    arr = url.split("?")[1].split('&')
    for item in arr:
        split = item.split('=')
        for i in range(len(split)):
            split[i] = split[i].lower()
        ans.append(split)
    return ans


def check_device_id(arr: list) -> bool:
    # 一般只会在key中标识
    sensitive_keys = ['device_id', 'deviceid']
    if len(arr) > 0:
        for sensitive_key in sensitive_keys:
            if arr[0].find(sensitive_key) != -1 and have_content(arr):
                return True
    return False


def check_ip_address(arr: list) -> bool:
    pattern = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
    mac_address = False
    has_ip_str = False
    for item in arr:
        if pattern.search(item) != None:
            mac_address = True
        if item.find('ip')!=-1:
            has_ip_str = True
    return mac_address and has_ip_str


def check_mac_address(arr: list) -> bool:
    pattern = re.compile(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})')
    for item in arr:
        if pattern.search(item) != None:
            return True
    return False


def get_packagename_version_by_appname(name: str):
    g = os.walk(r"E:\apk\type_top")
    for path, dir_list, file_list in g:
        for file_name in file_list:
            app_name = file_name.split('.')[0]
            if app_name != name:
                continue
            package_name, version_code, version_name = ak.get_apkid(os.path.join(path, file_name))
            return package_name, version_name
    return "", ""


if __name__ == '__main__':
    # str = 'https://h.huajiao.com/l/index?liveid=331263511&author=118777222&version=8.2.5.1026&userid=251436883&qd=%E5%A5%BD%E5%8F%8B%2F%E7%BE%A4%E7%BB%84'
    # if check_ip_address([str]):
    #     print('yes')
    # os.asdassd()


    conn = mysql()
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('data')
    ro = -1
    co = 0
    with open('files/ori_data.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cur = ''
        for row in reader:
            try:
                if len(row[2]) != 0:
                    ro += 1
                    co = 0
                    cur_app_name = row[2]
                    co += 1
                items = [row[7], row[10], row[13]]
                insert_new_data = False
                package_name, version_name = get_packagename_version_by_appname(cur_app_name)
                if package_name == '' or version_name == '':
                    continue
                print(package_name, version_name, cur_app_name)
                sql = "select * from url_leakage where package_name='{}' and version='{}'".format(package_name,
                                                                                                  version_name)
                if not conn.is_exit(sql):
                    sql = "insert into url_leakage(app_name, package_name, version) values('{}', '{}', '{}')".format(
                        cur_app_name, package_name,
                        version_name)
                    print(cur_app_name, '不存在')
                    conn.query(sql)
                # print(package_name, version_code, version_name)
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
                    # print('ori_url: ', ori_url)
                    arr = get_key_val(ori_url)
                    for k_v in arr:
                        if check_IMEI(k_v):
                            sql = "update url_leakage set IMEI='{}' where package_name='{}' and version='{}'".format(
                                1, package_name, version_name)
                            conn.query(sql)
                            print('have imei')

                        if check_ueser_logo(k_v):
                            sql = "update url_leakage set user_logo='{}' where package_name='{}' and version='{}'".format(
                                1, package_name, version_name)
                            conn.query(sql)
                            print('have user logo')

                        share_deive_arr = check_share_device(k_v)
                        if len(share_deive_arr) > 0:
                            sql = "update url_leakage set share_device='{}' where package_name='{}' and version='{}'".format(
                                ','.join(share_deive_arr), package_name, version_name)
                            conn.query(sql)
                            print('have share device: ', share_deive_arr)

                        share_platform_arr = check_share_platform(k_v)
                        if len(share_platform_arr) > 0:
                            sql = "update url_leakage set share_platform='{}' where package_name='{}' and version='{}'".format(
                                ','.join(share_platform_arr), package_name, version_name)
                            conn.query(sql)
                            print('have share platform: ', share_platform_arr)

                        if check_device_id(k_v):
                            sql = "update url_leakage set device_id='{}' where package_name='{}' and version='{}'".format(
                                1, package_name, version_name)
                            conn.query(sql)
                            print('have device id')
                        if check_ip_address(k_v):
                            sql = "update url_leakage set ip_address='{}' where package_name='{}' and version='{}'".format(
                                1, package_name, version_name)
                            conn.query(sql)
                            print('have ip address', k_v)
                        if check_mac_address(k_v):
                            sql = "update url_leakage set mac_address='{}' where package_name='{}' and version='{}'".format(
                                1, package_name, version_name)
                            conn.query(sql)
                            print('have mac address')
                    # print(arr)
                    # suh = Shortest_Url_Handler_Replace(ori_url)
                    # mes, url, similarity = suh.get_shortest_url_main()
                    co += 1
            except Exception as e:
                print(e)
        # workbook.save('data.xlsx')
