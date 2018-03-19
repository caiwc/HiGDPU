# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader
from weixin_scrapy.settings import SQL_DATETIME_FORMAT
from elasticsearch_tool.init_models import Weibo, Weixin, get_suggests
from elasticsearch.exceptions import NotFoundError
import datetime
from weixin_scrapy.utils import get_es_data


class TakeFirstScrapyLoader(ItemLoader):
    default_output_processor = TakeFirst()


def get_es_obj(model, obj_id):
    try:
        return model.get(id=obj_id)
    except NotFoundError:
        m = model()
        m._id = obj_id
        return m


class WeixinScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    id = scrapy.Field()
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
            self['id'], self['title'], self['publish_time'], now_time, self['url'],
            self['html_content'].encode('utf-8'),
            self.get('digest', ""),
            self.get('digest', ""), self['gzh']
        )
        return insert_sql, params

    def save_to_es(self):
        weixin = get_es_obj(Weixin, self['id'])
        weixin.title = self['title']
        weixin.url = self['url']
        weixin.cover = self.get('digest', "")
        weixin.digest = self.get('digest', "")
        weixin.content = get_es_data(self['html_content'])
        weixin.publish_time = self['publish_time']
        weixin.gzh = self['gzh']
        weixin.save()
        return


class WeiboScrapyItem(scrapy.Item):
    weibo_id = scrapy.Field()
    content = scrapy.Field()
    like = scrapy.Field()
    report = scrapy.Field()
    img = scrapy.Field()
    comment = scrapy.Field()
    large_img = scrapy.Field()
    publish_time = scrapy.Field()
    weibo_name = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into weibo(weibo_id,content,img,large_img,publish_time,likes,reports,weibo_name)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE likes=VALUES(likes),content=VALUES(content),
       reports=VALUES(reports),weibo_name=VALUES(weibo_name),publish_time=VALUES(publish_time),
        large_img=VALUES(large_img)
        """
        params = (
            self['weibo_id'], self['content'], self.get('img', ''), self.get('large_img', ''),
            self['publish_time'], self['like'], self['report'], self['weibo_name']
        )
        return insert_sql, params

    def save_to_es(self):
        weibo = get_es_obj(model=Weibo, obj_id=self['weibo_id'])
        weibo.content = self['content']
        weibo.publish_time = self['publish_time']
        weibo.comment = int(self['comment'])
        weibo.suggest = get_suggests(Weibo._doc_type.index, [(weibo.content, 10)], Weibo)
        weibo.save()
        return


class WeiboCommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    weibo = scrapy.Field()
    comment = scrapy.Field()
    publish_time = scrapy.Field()
    likes = scrapy.Field()
    author = scrapy.Field()
    reply_author = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into weibo_comment(comment_id,weibo,comment,publish_time,likes,author,reply_author)
                VALUES (%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE likes=VALUES(likes),reply_author=VALUES(reply_author)
              ,comment=VALUES(comment)
                """
        params = (
            self['comment_id'], self['weibo'], self['comment'].encode('utf-8'), self['publish_time'],
            self['likes'], self['author'], self.get('reply_author', ''),
        )
        return insert_sql, params

    def save_to_es(self):
        return


class OfficialItem(scrapy.Item):
    article_id = scrapy.Field()
    content = scrapy.Field()
    publish_time = scrapy.Field()
    title = scrapy.Field()
    img = scrapy.Field()
    url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into official(article_id,content,publish_time,title,img,url)
                VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content=VALUES(content), url=VALUES(url),img=VALUES(img)
                """
        params = (
            self['article_id'], self['content'], self['publish_time'],
            self['title'], self.get('img', ''), self['url']
        )
        return insert_sql, params
