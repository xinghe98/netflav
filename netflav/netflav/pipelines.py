import scrapy
import re
from scrapy.pipelines.images import ImagesPipeline
from netflav.downloader import download
import os
import time
from netflav.utils import utils
from netflav.dbs.db import sqldb

db = sqldb()


class netflixPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            lastid=int(sqldb().findflag()),
            folder=30,
        )

    def __init__(self, lastid, folder):
        self.lastid = lastid
        self.folder = folder
        self.foldername = self.mktimedir()

    def mktimedir(self):
        dirname = str(time.strftime('%Y%m%d%H%M'))
        try:
            os.makedirs(utils.dir+'/'+dirname)
        except Exception:
            pass
        return dirname

    def process_item(self, item, spider):
        # print(item)
        if self.lastid % self.folder == 0 and self.lastid != 0:
            self.foldername = self.mktimedir()
            item['foldername'] = self.foldername
        else:
            item['foldername'] = self.foldername
        self.lastid = self.lastid + 1
        if self.lastid < 10:
            dirname = '{}0{}'.format(utils.prefix, str(self.lastid))
        else:
            dirname = '{}{}'.format(utils.prefix, str(self.lastid))
        # 将文件名设置为 81xx.jpg 格式
        item['img_name'] = dirname
        # 将视频文件名设置为 -81xx-.mp4格式
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        video_name = re.sub(rstr, "_", item['title'])  # 替换为下划线
        if len(video_name) > 100:
            video_name = video_name[:100]
        item['video_name'] = '-{}-{}'.format(dirname, video_name)
        # self.lastid = self.lastid + 1
        print(self.lastid)
        return item


class netflixImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # if db.isExit(item['id']):
        yield scrapy.Request(item['cover'])
        # else:
        #     raise DropItem("该内容已经下载过"+item['id'])

    def file_path(self, request, response=None, info=None, *, item=None):
        # 将文件名设置为 81xx.jpg 格式
        filename = item['foldername']+'/' + item['img_name'] + '.jpg'
        return filename

    def item_completed(self, results, item, info):
        return item


class netflVideoPipeline(object):

    def process_item(self, item, spider):
        # print(item)
        # if item:
        download(item['video_url'], utils.dir + "/" +
                 item['foldername']+'/' + item['video_name']+'.mp4')
        db.inSert(item['id'])
