# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NetflavItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    cover = scrapy.Field()
    video_url = scrapy.Field()
    img_name = scrapy.Field()
    video_name = scrapy.Field()
    foldername = scrapy.Field()
    id = scrapy.Field()
    download = scrapy.Field()
