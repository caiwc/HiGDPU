from weixin_scrapy.spiders.weibo import WeiboSpider
from weixin_scrapy.spiders.weixin import WeixinSpider
from weixin_scrapy.spiders.official import OfficialSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def scrapy_crawl(spider):
    spider_dict = {
        'weixin': WeixinSpider,
        'weibo': WeiboSpider,
        "official": OfficialSpider
    }
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_dict[spider])
    process.start()

if __name__ == '__main__':
    scrapy_crawl('official')