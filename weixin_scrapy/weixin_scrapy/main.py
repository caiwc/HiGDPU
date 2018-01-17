from scrapy.cmdline import execute
import sys
import os

os.environ.setdefault('SCRAPY_SETTINGS_MODULE','weixin_scrapy.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


execute(['scrapy','crawl','weixin'])

# execute('scrapy crawl weibo -a start_page=1900 -a end_page=1920'.split(' '))