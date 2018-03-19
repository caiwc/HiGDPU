# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from scrapy.spiders.crawl import Request
from weixin_scrapy.items import TakeFirstScrapyLoader, OfficialItem
from weixin_scrapy.html_to_wxml import parser
from weixin_scrapy.utils import str_md5
import json


class OfficialSpider(scrapy.Spider):
    headers = {
        'referer': "http://www.gdpu.edu.cn",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    }
    cookies = """[
{
    "domain": "www.gdpu.edu.cn",
    "hostOnly": true,
    "httpOnly": false,
    "name": "DP_SESSIONID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "d22603f1:50",
    "id": 1
},
{
    "domain": "www.gdpu.edu.cn",
    "hostOnly": true,
    "httpOnly": false,
    "name": "PHPSESSID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "5qrvv8a7j0qvi64hqap1351275",
    "id": 2
}
]"""
    name = 'official'
    base_url = 'http://www.gdpu.edu.cn'
    allowed_domains = ['http://www.gdpu.edu.cn']
    start_urls = ['http://www.gdpu.edu.cn/index.php?s=/home/newscenter/lists/category/yw.html',
                  'http://www.gdpu.edu.cn/index.php?s=/home/newscenter/lists/category/xwzh.html',
                  'http://www.gdpu.edu.cn/index.php?s=/home/newscenter/lists/category/fc.html']

    custom_settings = {
        'ITEM_PIPELINES': {
            'weixin_scrapy.pipelines.MysqlTwistedPipeline': 200,
        }

    }

    def get_cookies(self):
        return json.loads(self.cookies)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, headers=self.headers, cookies=self.get_cookies())

    def parse(self, response):
        article_list = response.xpath('//*[@id="contents"]/div[2]/div/li/a/@href').extract()
        for link in article_list:
            url = urljoin(self.base_url, link)
            yield Request(url=url, callback=self.article_parse, headers=self.headers, cookies=self.get_cookies(),
                          dont_filter=True)

    def article_parse(self, response):
        resp = parser(response.text)
        item_loader = TakeFirstScrapyLoader(item=OfficialItem(), response=response)
        item_loader.add_value('article_id', str_md5(resp.title))
        item_loader.add_value('title', resp.title)
        item_loader.add_value('publish_time', resp.publish_date)
        item_loader.add_value('content', "<partition>".join(resp.content))
        item_loader.add_value('img', "<partition>".join(resp.img))
        item_loader.add_value('url', response.url)
        yield item_loader.load_item()
