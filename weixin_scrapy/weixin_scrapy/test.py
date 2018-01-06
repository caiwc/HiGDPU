from scrapy.selector import Selector

html =""""""

res = Selector(text=html)


weibo_list = res.xpath('//*[starts-with(@id,"M_")]')

for weibo in weibo_list:
    print(weibo)