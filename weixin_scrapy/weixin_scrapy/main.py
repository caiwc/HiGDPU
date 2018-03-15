from scrapy.cmdline import execute
import sys
import os


def run(spider):
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'weixin_scrapy.settings')
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    if spider == 'weixin':
        execute(['scrapy', 'crawl', 'weixin'])
    elif spider == 'weibo':
        execute('scrapy crawl weibo -a start_page=1 -a end_page=10'.split(' '))
    elif spider == 'official':
        execute(['scrapy', 'crawl', 'official'])


if __name__ == '__main__':
    run(spider='weixin')
