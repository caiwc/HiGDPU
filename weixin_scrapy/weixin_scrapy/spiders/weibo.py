# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from pydispatch import dispatcher
import json
from random import choice
import re
import time
from weixin_scrapy import settings
from weixin_scrapy.items import TakeFirstScrapyLoader, WeiboScrapyItem
from weixin_scrapy.utils import time_str_format


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://weibo.cn/']
    weibo_host = start_urls[0]
    search_query = ['gdpuwbl', 'gdpuhome']

    cookies_list = ["""[
{
    "domain": ".weibo.cn",
    "expirationDate": 1515492644.087834,
    "hostOnly": false,
    "httpOnly": true,
    "name": "_T_WL",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 1
},
{
    "domain": ".weibo.cn",
    "expirationDate": 1517132302.386672,
    "hostOnly": false,
    "httpOnly": true,
    "name": "_T_WM",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "520649644978ef5fcf27b56056241ea8",
    "id": 2
},
{
    "domain": ".weibo.cn",
    "expirationDate": 1517998244.089478,
    "hostOnly": false,
    "httpOnly": true,
    "name": "_WEIBO_UID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1770147732",
    "id": 3
},
{
    "domain": ".weibo.cn",
    "expirationDate": 1830766722.010782,
    "hostOnly": false,
    "httpOnly": true,
    "name": "SCF",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "Ap-TmQ2Pbdze05SdNnxC_-uaJT8975cTm4T-N5WL7_uPnMJMgwGZtHjku2Yi03TJ8HX_yTlqEhZz5eajYVRkM4w.",
    "id": 4
},
{
    "domain": ".weibo.cn",
    "hostOnly": false,
    "httpOnly": false,
    "name": "SSOLoginState",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "1515406721",
    "id": 5
},
{
    "domain": ".weibo.cn",
    "expirationDate": 1546942722.011794,
    "hostOnly": false,
    "httpOnly": true,
    "name": "SUB",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "_2A253VzXRDeThGeRM61EQ9yvMyD6IHXVUuFuZrDV6PUJbktANLVbgkW1NU-H9MncojPU8ctdi2X-hPb72xi3DEM8a",
    "id": 6
},
{
    "domain": ".weibo.cn",
    "expirationDate": 1546942722.012101,
    "hostOnly": false,
    "httpOnly": false,
    "name": "SUBP",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh9izAqoHi9uGUyNuFr0u_15JpX5K-hUgL.FozEehepS0-7e0z2dJLoI79zI-U2-8-t",
    "id": 7
},
{
    "domain": ".weibo.cn",
    "expirationDate": 1546942722.012404,
    "hostOnly": false,
    "httpOnly": false,
    "name": "SUHB",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "03oUaxidOv9Ymy",
    "id": 8
}
]"""]

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        'host': "weibo.cn",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    }

    start_page = 2075
    end_page = 3000

    re_like = re.compile("赞\[(\d+)]")
    re_report = re.compile("转发\[(\d+)]")
    re_comment = re.compile("评论\[(\d+)]")

    def __init__(self):
        super(WeiboSpider, self).__init__()
        from scrapy import signals
        dispatcher.connect(self.spider_close, signals.spider_closed)

    def spider_close(self, spider):
        from qyweixin.qyweixin_api import send_weixin_message, qyweixin_text_type
        print("关闭spider")
        info = "微博爬虫结束,爬至{}页".format(self.end_page)
        send_weixin_message(send_type=qyweixin_text_type, msg_content=info)

    def get_cookies(self):
        return json.loads(choice(self.cookies_list))

    def start_requests(self):
        for item in self.search_query:
            cookies = self.get_cookies()
            yield Request(url=self.weibo_host + item + '?page={}'.format(self.start_page), headers=self.headers,
                          cookies=cookies, callback=self.parse,
                          meta={'page': self.start_page, 'name': item})

    def parse(self, response):
        current_page = response.meta.get('page')
        pages = response.meta.get('max_page', None)
        name = response.meta.get('name')
        if current_page == self.start_page and not pages:
            if current_page == 1:
                tmp = '2'
            else:
                tmp = '4'
            pages_str = response.xpath('//*[@id="pagelist"]/form/div/text()[{}]'.format(tmp)).extract_first("")
            pages = re.findall(".*?/(\d+)页", pages_str)
            print(pages)
            pages = int(pages[0])

        weibo_list = response.xpath('//*[starts-with(@id,"M_")]')
        for weibo in weibo_list:
            item_loader = TakeFirstScrapyLoader(item=WeiboScrapyItem(), selector=weibo)
            time_str = weibo.xpath('.//div[last()]/span[@class="ct"]/text()').extract_first("")
            item_loader.add_value('publish_time', time_str_format(time_str=time_str))
            item_loader.add_xpath('content', './/div/span[@class="ctt"]/text()[1]')
            item_loader.add_xpath('weibo_id', '@id')
            item_loader.add_xpath('img', './/img[@class="ib"]/@src')
            item_loader.add_value('weibo_name', name)
            meta_list = weibo.xpath('.//div[last()]/a/text()').extract()
            for meta in meta_list:
                if self.re_comment.match(meta):
                    item_loader.add_value('comment', int(self.re_comment.match(meta).group(1)))
                elif self.re_like.match(meta):
                    item_loader.add_value('like', int(self.re_like.match(meta).group(1)))
                elif self.re_report.match(meta):
                    item_loader.add_value('report', int(self.re_report.match(meta).group(1)))
            time.sleep(settings.WEIBO_SLEEP_TIME)
            yield item_loader.load_item()

        if isinstance(pages, int) and (int(current_page) < pages or int(current_page) < self.end_page):
            next_page = int(current_page) + 1
            next_url = self.weibo_host + name + '?page={}'.format(str(next_page))
            cookies = self.get_cookies()
            yield Request(url=next_url, headers=self.headers, cookies=cookies, callback=self.parse,
                          meta={'page': next_page, 'name': name, 'max_page': pages})
