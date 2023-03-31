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
    def __init__(self):
        self.flag = 1
        self.folder = 30
        self.foldername = self.mktimedir()

    def mktimedir(self):
        foldername = str(time.strftime('%Y%m%d%H%M'))
        try:
            os.makedirs(utils.dir+'/'+foldername)
        except Exception:
            pass
        return foldername

    def process_item(self, item, spider):
        # print(item)
        if self.flag < 10:
            dirname = '{}0{}'.format(utils.prefix, self.flag)
        else:
            dirname = '{}{}'.format(utils.prefix, self.flag)
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
        if db.isExit(item['id']):
            yield scrapy.Request(item['cover'])
        else:
            print("该内容已经下载过"+item['id'])
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
        if db.isExit(item['id']):
            # if item:
            download(item['video_url'], utils.dir + "/" +
                     item['foldername']+'/' + item['video_name']+'.mp4')
            db.inSert(item['id'])
        return item
