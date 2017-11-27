# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from weixin_scrapy import settings
import re
import json
import logging
from urllib import parse

class WeixinSpider(scrapy.Spider):
    name = 'weixin'
    allowed_domains = ['weixin.sogou.com/']
    wx_art_domains = ['https://mp.weixin.qq.com']
    search_gzh_url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
    start_urls = []
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Cookie': 'ssuid=6768833500; SUV=00EB21C8DF4945D157CFDBE060AC5080; SUID=C39D68CA142D900A5530C134000EBC84; LSTMV=396%2C27; LCLKINT=6281; ABTEST=0|1509630197|v1; weixinIndexVisited=1; SNUID=CE681B8E52570C6FD59D3411520A6F63; IPLOC=CN4401; sct=8; JSESSIONID=aaa5AbVYx1plkefP4Gv8v',
               'Host': 'weixin.sogou.com',
               'RA-Sid': 'CA689DC5-20150327-161514-0c9bb8-ebe4f5',
               'RA-Ver': '3.0.7',
               'Referer': 'http://weixin.sogou.com/',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
               }

    gzh_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Host': 'mp.weixin.qq.com',

    }

    # def __init__(self):
    #     self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
    #     super(WeixinSpider, self).__init__()
    #     dispatcher.connect(self.spider_close, signals.spider_closed)
    #
    # def spider_close(self,spider):
    #     print("关闭spider")
    #     self.browser.quit()


    def start_requests(self):
        gzh_dict = settings.GZH_DICT
        for gzh in gzh_dict:
            url = self.search_gzh_url.format(gzh)
            yield Request(url=url, dont_filter=True, callback=self.gzh_host_parse, headers=self.headers,
                          meta={'gzh': gzh})

    def gzh_host_parse(self, response):
        gzh = response.meta.get('gzh')
        logging.info("parse the {}".format(gzh))
        gzh_host_url = response.css('#sogou_vr_11002301_box_0 .gzh-box2 .txt-box .tit a::attr(href)').extract_first("")
        if gzh_host_url:
            yield Request(url=gzh_host_url, dont_filter=True, callback=self.gzh_article_parse, headers=self.gzh_headers,
                          meta={'gzh': gzh})

    def gzh_article_parse(self, response):
        gzh = response.meta.get('gzh')
        logging.info("parse the {} host".format(gzh))
        script_text = response.xpath('/html/body/script[6]/text()').extract_first("")
        mg_list_check = re.search('.*?msgList\s=\s(.*?}]});', script_text)
        if mg_list_check:
            mg_list = mg_list_check.group(1)
            mg_list = json.loads(mg_list)
            if 'list' in mg_list:
                for art_item in mg_list['list']:
                    art_url = art_item['app_msg_ext_info']['content_url']
                    art_url = parse.urljoin(self.wx_art_domains[0], art_url)
                    art_url.replace('amp;','')
                    art_title = art_item['app_msg_ext_info']['title']
                    yield Request(url=art_url, dont_filter=True, callback=self.parse, headers=self.gzh_headers,
                                  meta={'title': art_title, 'gzh': gzh})

    def parse(self, response):
        gzh = response.meta.get('gzh')
        title = response.meta.get('title')
        logging.info("parse the {0} {1}".format(gzh, title))
        article_content = response.css('#img-content').extract_first("")
