import scrapy
import re
from scrapy.pipelines.images import ImagesPipeline
from netflav.downloader import download
import os
import time


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
        print(self.flag)
        if self.flag < 10:
            dirname = '810{}'.format(self.flag)
        else:
            dirname = '81{}'.format(self.flag)
        self.flag += 1
        # 将文件名设置为 81xx.jpg 格式
        item['img_name'] = dirname
        item['foldername'] = self.foldername
        # 根据文件数量，创建文件夹
        if self.flag % self.folder == 0:
            item['foldername'] = self.mktimedir()
        # 将视频文件名设置为 -81xx-.mp4格式
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        video_name = re.sub(rstr, "_", item['title'])  # 替换为下划线
        if len(video_name) > 100:
            video_name = video_name[:100]
        item['video_name'] = '-{}-{}'.format(dirname, video_name)
        return item


class netflixImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['cover'])

    def file_path(self, request, response=None, info=None, *, item=None):
        # 将文件名设置为 81xx.jpg 格式
        filename = item['foldername']+'/' + item['img_name'] + '.jpg'
        # print('正在下载'+filename)
        return filename

    def item_completed(self, results, item, info):
        return item


class netflVideoPipeline(object):

    def process_item(self, item, spider):
        # print(item)
        download(item['video_url'], "./content/" +
                 item['foldername']+'/' + item['video_name']+'.mp4')
        return item
