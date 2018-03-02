from scrapy.cmdline import execute
import sys
import os


def run(spider):
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'weixin_scrapy.settings')
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    if spider == 'weixin':
        execute(['scrapy', 'crawl', 'weixin'])
    elif spider == 'weibo':
        execute('scrapy crawl weibo -a start_page=50 -a end_page=152'.split(' '))


if __name__ == '__main__':
    run(spider='weibo')