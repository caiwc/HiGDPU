# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader

class WeixinScrapyLoader(ItemLoader):
    default_output_processor = TakeFirst()

class WeixinScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    title_md5 = scrapy.Field()
    html_content = scrapy.Field()
    publish_time = scrapy.Field()
    cover = scrapy.Field()
    digest = scrapy.Field()
    url = scrapy.Field()
