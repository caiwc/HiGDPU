from scrapy.cmdline import execute
import sys
import os

os.environ.setdefault('SCRAPY_SETTINGS_MODULE','weixin_scrapy.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


execute(['scrapy','crawl','weixin'])

