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
    gzh = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into weixin_gzh(title_md5,title,publish_time,url,html_content,cover,digest,gzh) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE html_content=VALUES(html_content),cover=VALUES(cover),digest=VALUES(digest),gzh=VALUES(gzh),url=VALUES(url)
        """

        params = (
            self['title_md5'], self['title'], self['publish_time'], self['url'], self['html_content'].encode('utf-8'),
            self.get('cover', ""),
            self.get('digest', ""), self['gzh']
        )
        return insert_sql, params
