from netflav.utils import utils
import pymysql


class sqldb(object):
    def __init__(self):
        self.mysql_host = utils.host
        self.mysql_user = utils.user
        self.mysql_password = utils.passwd
        self.mysql_db = utils.db
        self.mysql_port = utils.port
        self.mysql_db_charset = 'utf8mb4'
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                    port=self.mysql_port,
                                    password=self.mysql_password,
                                    db=self.mysql_db,
                                    charset=self.mysql_db_charset,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.conn.cursor().execute('CREATE DATABASE IF NOT EXISTS %s;' % self.mysql_db)
        self.conn.cursor().execute(
            'create table if not exists %s(id int auto_increment primary key not null, %s varchar(20));' % (utils.table, utils.field))
        self.conn.select_db(self.mysql_db)
        self.cursor = self.conn.cursor()

    def isExit(self, id) -> bool:
        sql = 'select 1 from %s where %s = "%s" limit 1;' % (
            utils.table, utils.field, id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            # 可以下载
            return True
        if len(result) != 0:
            return False

    def inSert(self, value):
        try:
            sql = 'INSERT INTO %s (%s) VALUES ("%s")' % (
                utils.table, utils.field, value)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception:
            print("数据库写入失败")

        # def close_spider(self, spider):
        #     self.conn.close()
        #     self.cursor.close()
