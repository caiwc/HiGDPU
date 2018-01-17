# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader
from weixin_scrapy.settings import SQL_DATETIME_FORMAT

import datetime


class TakeFirstScrapyLoader(ItemLoader):
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
    gzh = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into weixin__gzh(title_md5,title,publish_time,scrapy_time,url,html_content,cover,digest,gzh)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE html_content=VALUES(html_content),
        cover=VALUES(cover),digest=VALUES(digest),gzh=VALUES(gzh),url=VALUES(url),scrapy_time=VALUES(scrapy_time)
        """
        now_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        params = (
            self['title_md5'], self['title'], self['publish_time'], now_time, self['url'],
            self['html_content'].encode('utf-8'),
            self.get('cover', ""),
            self.get('digest', ""), self['gzh']
        )
        return insert_sql, params


class WeiboScrapyItem(scrapy.Item):
    weibo_id = scrapy.Field()
    content = scrapy.Field()
    like = scrapy.Field()
    comment = scrapy.Field()
    report = scrapy.Field()
    img = scrapy.Field()
    publish_time = scrapy.Field()
    weibo_name = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into weibo(weibo_id,content,img,publish_time,likes,comments,reports,weibo_name)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE likes=VALUES(likes),
        comments=VALUES(comments),reports=VALUES(reports),weibo_name=VALUES(weibo_name),publish_time=VALUES(publish_time)
        """
        params = (
            self['weibo_id'], self['content'].encode('utf-8'), self.get('img', ''), self['publish_time'],
            self['like'], self['comment'], self['report'],self['weibo_name']
        )
        return insert_sql, params
