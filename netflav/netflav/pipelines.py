import scrapy
import re
from scrapy.pipelines.images import ImagesPipeline
from netflav.downloader import download
import os
import time
from netflav.utils import utils
import pymysql


class netflixPipeline(object):
    def __init__(self):
        self.flag = 1
        self.folder = 30
        self.foldername = self.mktimedir()

    def mktimedir(self):
        foldername = str(time.strftime('%Y%m%d%H%M'))
        try:
            os.makedirs('./content/'+foldername)
        except Exception:
            pass
        return foldername

    def process_item(self, item, spider):
        # print(item)
        if self.flag < 10:
            dirname = '810{}'.format(self.flag)
        else:
            dirname = '81{}'.format(self.flag)
        self.flag += 1
        # 将文件名设置为 81xx.jpg 格式
        item['img_name'] = dirname
        item['foldername'] = self.foldername
        # 根据文件数量，创建文件夹
        if (self.flag-2) % self.folder == 0:
            self.foldername = self.mktimedir()
            item['foldername'] = self.foldername
        # 将视频文件名设置为 -81xx-.mp4格式
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        video_name = re.sub(rstr, "_", item['title'])  # 替换为下划线
        if len(video_name) > 100:
            video_name = video_name[:100]
        item['video_name'] = '-{}-{}'.format(dirname, video_name)
        return item


class netflixImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['download'] == 1:
            yield scrapy.Request(item['cover'])
        else:
            return item

    def file_path(self, request, response=None, info=None, *, item=None):
        # 将文件名设置为 81xx.jpg 格式
        filename = item['foldername']+'/' + item['img_name'] + '.jpg'
        return filename

    def item_completed(self, results, item, info):
        return item


class netflVideoPipeline(object):

    def process_item(self, item, spider):
        # print(item)
        if item['download'] == 1:
            download(item['video_url'], "./content/" +
                     item['foldername']+'/' + item['video_name']+'.mp4')
        return item


class MySQLPipeline(object):
    def __init__(self):
        self.mysql_host = utils.host
        self.mysql_user = utils.user
        self.mysql_password = utils.passwd
        self.mysql_db = utils.db
        self.mysql_db_charset = 'utf8'
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                    password=self.mysql_password,
                                    db=self.mysql_db, charset=self.mysql_db_charset)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'select 1 from infoid where id = "%s" limit 1;' % (item['id'])
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            sql = 'INSERT INTO infoid (id) VALUES ("%s")' % (item['id'])
            self.cursor.execute(sql)
            self.conn.commit()
            item['download'] = 1
        if len(result) != 0:
            item['download'] = 0
        return item

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()
