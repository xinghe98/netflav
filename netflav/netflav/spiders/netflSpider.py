import scrapy
import json
from netflav.items import NetflavItem
import re


class NetflspiderSpider(scrapy.Spider):
    name = "netflSpider"
    allowed_domains = ["netflav.com", "streamtape.to"]
    start_urls = ["https://netflav.com/uncensored"]

    # 获取视频列表页的所有视频链接
    def parse(self, response):
        data = response.xpath(
            '//div[@class="video_grid_container"]/div//a[1]/@href').getall()
        for uri in data:
            video_url = 'https://netflav.com'+uri
            # 从视频链接中获取视频信息
            yield scrapy.Request(video_url, callback=self.parse_video)

        for i in range(2, 5):
            url = self.start_urls[0] + '?page={}'.format(str(i))
            yield scrapy.Request(url=url, callback=self.parse)

    # 获取视频部分信息
    def parse_video(self, response):
        data = response.xpath(
            '//script').re(r'<script id="__NEXT_DATA__" type="application/json">(.*)</script>')[0]
        data = json.loads(data)
        # 获取视频id
        id = data['props']['initialState']['video']['data']['videoId']
        # 获取视频标题
        title = data['props']['initialState']['video']['data']['description']
        # 获取视频封面
        cover = data['props']['initialState']['video']['data']['preview']
        # 获取所有可播放的源
        src_video = data['props']['initialState']['video']['data']['srcs']
        # 从列表内取出含有字符串‘streamtape.to/e‘的元素,即ST的播放源
        try:
            video_ST = [i for i in src_video if 'streamtape.to/e' in i][0]
            if video_ST is not None and video_ST != '':
                yield scrapy.Request(video_ST,
                                     callback=self.parse_url,
                                     meta={'title': title, 'cover': cover,
                                           'id': id})
        except IndexError:
            print('ST视频链接获取失败')

    # 获取视频播放链接
    def parse_url(self, response):
        # 这个url是token不正确的url，token需要另外获取
        raw_data = response.xpath('//div[@id="robotlink"]/text()').get()
        # print(raw_data)
        # 正则匹配出假token
        token = re.findall(r'&token=(.*e)', raw_data)[0]
        # 替换url中的token
        video_url = raw_data.replace(token, '')
        # print(video_url)
        # 获取真正的token
        token = response.xpath(
            '//script').re(r'&token=(.*)\'')

        video_url = video_url + token[0]
        # 获取视频播放链接
        item = NetflavItem()
        item['title'] = response.meta['title']
        item['id'] = response.meta['id']
        item['cover'] = response.meta['cover']
        item['video_url'] = 'https:/' + video_url
        yield item
