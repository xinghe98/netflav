from netflav.utils import utils
import pymysql


class sqldb(object):
    def __init__(self):
        self.mysql_host = utils.host
        self.mysql_user = utils.user
        self.mysql_password = utils.passwd
        self.mysql_db = utils.db
        self.mysql_port = utils.port
        self.mysql_db_charset = 'utf8'
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                    port=self.mysql_port,
                                    password=self.mysql_password,
                                    db=self.mysql_db,
                                    charset=self.mysql_db_charset)
        self.cursor = self.conn.cursor()

    def isExit(self, id) -> bool:
        sql = 'select 1 from %s where id = "%s" limit 1;' % (
            utils.table, id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            # 可以下载
            return True
        if len(result) != 0:
            return False

    def inSert(self, value):
        try:
            sql = 'INSERT INTO %s (id) VALUES ("%s")' % (
                utils.table, value)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception:
            print("数据库写入失败")

        # def close_spider(self, spider):
        #     self.conn.close()
        #     self.cursor.close()