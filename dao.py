import sys, pymysql, traceback
import time, os, yaml


class mysql:
    def __init__(self):
        # 获取文件全路径
        filename = os.path.join(os.getcwd(), 'config', 'confi.yaml').replace("\\", "/")
        file = open(filename, 'r', encoding='utf-8')
        file_data = file.read()
        data = yaml.load(file_data, Loader=yaml.FullLoader)
        self.host = data['mysql_confi']['host']
        self.user = data['mysql_confi']['user']
        self.passwd = str(data['mysql_confi']['passwd'])
        self.db = data['mysql_confi']['db']
        self.port = data['mysql_confi']['port']
        self.charset = data['mysql_confi']['charset']
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            self.conn = pymysql.Connection(host=self.host, user=self.user, password=self.passwd, database=self.db,
                                           port=self.port, charset=self.charset)
            return True
        except pymysql.Error as e:
            return False

    def _reConn(self, num=28800, stime=3):  # 重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()  # cping 校验连接是否异常
                _status = False
            except Exception as e:
                if self._conn() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                print('连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束， e: ', e)
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    def is_exit(self, sql='') -> bool:
        try:
            self._reConn()
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) == 0:
                return False
            self.cursor.close()
            return True
        except pymysql.Error as e:
            print('sql:{}, error:{}'.format(sql, e))
            return False

    def select(self, sql=''):
        try:
            self._reConn()
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.cursor.close()
            return result
        except pymysql.Error as e:
            print('sql:{}, error:{}'.format(sql, e))
            return False

    def select_limit(self, sql='', offset=0, length=20):
        sql = '%s limit %d , %d ;' % (sql, offset, length)
        return self.select(sql)

    def query(self, sql=''):
        try:
            self._reConn()
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute("set names utf8")  # utf8 字符集
            result = self.cursor.execute(sql)
            # print(sql)
            self.conn.commit()
            self.cursor.close()
            return (True, result)
        except pymysql.Error as e:
            print('sql:{}, error:{}'.format(sql, e))
            return False

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    con = mysql()
    con.query('insert into student(name, age) values("caizhaoxin", 22)')
