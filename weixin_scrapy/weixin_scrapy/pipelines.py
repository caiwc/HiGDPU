# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from os import path
import re
import hashlib
from scrapy.utils.python import to_bytes


class WeixinScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)
        print(item)
        spider.logger.exception(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class ElasticSearchPipeline(object):
    def process_item(self, item, spider):
        item.save_to_es()
        return item


class HtmlPipeline(object):
    def __init__(self, template_path):
        self.template_path = template_path

    @classmethod
    def from_settings(cls, settings):
        project_path = settings['PROJECT_PATH']
        template_path = path.join(project_path, 'web', 'templates')
        return cls(template_path)

    def format_url(self, url):
        prefix = "../static/full/"
        return "{}{}.jpg".format(prefix, hashlib.sha1(to_bytes(url)).hexdigest())

    def process_item(self, item, spider):
        html = item.get('html_content', '')
        article_id = item.get('id')
        file_path = path.join(self.template_path, "{}.html".format(article_id))
        src = "&tp=webp&wxfrom=5&wx_lazy=1"
        find_img = re.compile('(data-src)')
        img_list = re.findall('"(https://mmbiz.qpic.*?)"', html)
        item['article_img'] = img_list
        print(img_list)
        if html:
            new_html = find_img.sub('src', html)
            for img in img_list:
                new_html = new_html.replace(img,self.format_url(img))
            f = open(file_path, 'w+')
            f.write(new_html)
            f.close()
        return item


class ArticleImagePipeline(ImagesPipeline):
    pass
