# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    username = scrapy.Field()
    dateModified = scrapy.Field()
    content = scrapy.Field()
    personalInfo = scrapy.Field()
    pass
