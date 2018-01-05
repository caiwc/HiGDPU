from weixin_scrapy.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
import re
import datetime


def str_md5(text):
    import hashlib
    return hashlib.new('md5', (text).encode('utf-8')).hexdigest()


def timestampe_to_time(timestamp):
    import time
    st = time.localtime(timestamp)
    return time.strftime(SQL_DATETIME_FORMAT, st)


def time_str_format(time_str):
    time_list = time_str.split()
    if len(time_list) == 3:
        if re.match('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', time_list[0] + ' ' + time_list[1]):
            return time_list[0] + ' ' + time_list[1]
        if time_list[0].startswith('今天') and re.match('\d{2}:\d{2}', time_list[1]):
            today = datetime.date.today().strftime(SQL_DATE_FORMAT)
            return today + ' ' + time_list[1] + ':00'
        re_date = re.match('(\d{2})月(\d{2})日', time_list[0])
        if re_date and re.match('\d{2}:\d{2}', time_list[1]):
            year = datetime.date.today().year
            date = re_date.groups(1)
            return str(year) + "-" + date[0] + '-' + date[1] + ' ' + time_list[1] + ':00'
    elif len(time_list) == 2 and time_list[0].endswith('分钟前'):
        re_time = re.match('(\d+)分钟前', time_list[0])
        now = datetime.datetime.today() - datetime.timedelta(minutes=int(re_time.group(1)))
        return now.strftime(SQL_DATETIME_FORMAT)
    return datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)


item_dict = {"list": [{"app_msg_ext_info": {"author": "", "content": "",
                                            "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7gn4rdtWAwEJq23f3WOJ*gzHGI*hrOIFOJOCJCAFD-LWovva3r0Qd6VgZXFNrAs81WD1gH8E7xij9EO9NyUL0-k=",
                                            "copyright_stat": 100,
                                            "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/hp6WA88JQ4Tbd42ZSicMCHDG4KUo6mrOIeJWTF2JZTWnYMGKv6oRYeXxdquKCiaD85nwib6GC0k5PlQQ1YhR9Pg0g/0?wx_fmt=jpeg",
                                            "del_flag": 1,
                                            "digest": "数据科学、Web 开发和机器学习等都可以使用 Python 来开发。Quora、Pinterest 和 Spotify 都使用 Python 来进行他们的后端 Web 开发。来学习一下 Python 吧。",
                                            "fileid": 0, "is_multi": 0, "multi_app_msg_item_list": [],
                                            "source_url": "https://www.oschina.net/translate/learning-python-from-zero-to-hero?lang=chs&amp;page=2#",
                                            "subtype": 9, "title": "从 Zero 到 Hero ，一文掌握 Python"},
                       "comm_msg_info": {"content": "", "datetime": 1511925793, "fakeid": "3098539049",
                                         "id": 1000000234, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7n7tsddt8VPd30o2VLmTO0K1E7KCZDDoDND59JtE0cWkBuncqp1eRwCS-kHVo4h3PHTQHv4gnrLq0DDVFGKIAeU=",
                                               "copyright_stat": 100,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/hp6WA88JQ4Tbd42ZSicMCHDG4KUo6mrOIfqeOLNfb21kWmNsJHTlrZq7jOfLDtKN4w4E37dRNZOs80NYoRD9pGw/0?wx_fmt=jpeg",
                                               "del_flag": 1,
                                               "digest": "如何从众多的Python GUI框架和工具包中进行选择是个头疼的问题，整理推荐四个开发工具包（Gtk、Qt、Tk和wxwidgets）以及七个优秀框架供广大开发者参考。",
                                               "fileid": 0, "is_multi": 0, "multi_app_msg_item_list": [],
                                               "source_url": "http://www.ctocio.com/ccnews/25373.html", "subtype": 9,
                                               "title": "2017年最棒的七个Python图形应用GUI开发框架"},
                          "comm_msg_info": {"content": "", "datetime": 1511837384, "fakeid": "3098539049",
                                            "id": 1000000233, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "刘欣", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7ljyQvtNBO0ePXkUhZCzvhI*btmjl*6LL8Lylsb5CS4sULDOfVv5eYhaYWXXyFJTCE0B*FE*56Y-5GovHI2A6g4=",
                                               "copyright_stat": 101,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/KyXfCrME6ULpErm3bCbn30sq8xsn46BFibcPx1wnRYPicuA0IMO8u6120VtDGmfcicqP4L1XdIMaUEmx0UG5C9UBw/0?wx_fmt=jpeg",
                                               "del_flag": 1, "digest": "分布式、集群、负载均衡、单点失败、失效转移.... 大解密", "fileid": 0,
                                               "is_multi": 0, "multi_app_msg_item_list": [], "source_url": "",
                                               "subtype": 9, "title": "小白科普：分布式和集群"},
                          "comm_msg_info": {"content": "", "datetime": 1511753966, "fakeid": "3098539049",
                                            "id": 1000000232, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7rb8SoRQt7UHeUDTdSSi*u4vlmuUCW-OZgoATXQYzr1qaCifFpb0iTIWhpwGZ8SxXao58XZoDG1d-D2aPCICFQk=",
                                               "copyright_stat": 100,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/KmXPKA19gWic2S6HibOSyZeYuEp5lKDqbXddgicIZ7qQd6bcAQmbicicZk1fcr1yf8cKfFIic6nMYY8zCicLJmGyELu6g/0?wx_fmt=jpeg",
                                               "del_flag": 1,
                                               "digest": "前段时间，Python Files 博客发布了几篇主题为「Hunting Performance in Python Code」的系列文章，对提升 Python 代码的性能的方法进行了介绍。",
                                               "fileid": 0, "is_multi": 0, "multi_app_msg_item_list": [],
                                               "source_url": "http://mp.weixin.qq.com/s/5xs1ivkrUAP_Rr9P-EMc5g",
                                               "subtype": 9, "title": "代码优化指南：人生苦短，我用Python"},
                          "comm_msg_info": {"content": "", "datetime": 1511493886, "fakeid": "3098539049",
                                            "id": 1000000231, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7hPnSmVKO8waVkXXeM7VUf8qOZVAin1OhxLU2iRq-BpAsQpg*q742jnCdvpmvpz7NJEq721gm-daysdL1gGJ0ug=",
                                               "copyright_stat": 100,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/iciaMJDiaNTbG7SaxWJV0m1macSLOgDOm9mQuYaq8SYnlbgSxibn4vydNhpia83dt8Q5W9scGibe1aCWgD4wgrNq6NXA/0?wx_fmt=jpeg",
                                               "del_flag": 1, "digest": "本文主要从环境设置和内存分析两个方面探讨Python代码优化的路径。",
                                               "fileid": 504205228, "is_multi": 0, "multi_app_msg_item_list": [],
                                               "source_url": "https://mp.weixin.qq.com/s/hP5Mqz_jvgv-iLn7afJ1JQ",
                                               "subtype": 9, "title": "Python代码优化指南：从环境设置到内存分析"},
                          "comm_msg_info": {"content": "", "datetime": 1511403401, "fakeid": "3098539049",
                                            "id": 1000000230, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7qAy4GHFCsoOc6-F*xdQkxJnvVBdTsi5O2w69oc5GpC9Tceg38O-ik7CvaivibvZ98I7MpS5bxr599FOqaarOKA=",
                                               "copyright_stat": 100,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/fhujzoQe7TroPtkv7JAzSye7cTgCWjcQQkJRFpul1elDBHdSE1QeLXQuTUW65JtricUYCXNQL1O06smZOuObGTg/0?wx_fmt=jpeg",
                                               "del_flag": 1, "digest": "怎样在家用 Python 和树莓派搭建一个家用便携的自制酿啤酒装置?",
                                               "fileid": 0, "is_multi": 0, "multi_app_msg_item_list": [],
                                               "source_url": "https://linux.cn/article-8942-1.html", "subtype": 9,
                                               "title": "用 Linux、Python 和树莓派酿制啤酒"},
                          "comm_msg_info": {"content": "", "datetime": 1511319431, "fakeid": "3098539049",
                                            "id": 1000000229, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7lxqcGqQ9ng71t9Qa0vW7J2aqD6CKZLvA2dJz7o9zHs41t3vVNh2Zo8s6fBaJR1SshU5F-AVtz8ISOrqKhzkq*A=",
                                               "copyright_stat": 100,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/hp6WA88JQ4QKLaGoPYBcVjemgfcDDElf6XJ3XaWNDLEGQsZnSHsaTp7O28fvABzQKwp8DK5WK5U7GAlZYyAUicA/0?wx_fmt=jpeg",
                                               "del_flag": 1, "digest": "整理了 Google 开源的热门项目，排名顺序按照 Github ★Star 数排列。",
                                               "fileid": 0, "is_multi": 0, "multi_app_msg_item_list": [],
                                               "source_url": "https://www.itcodemonkey.com/article/329.html",
                                               "subtype": 9, "title": "开源巨献：Google最热门60款开源项目"},
                          "comm_msg_info": {"content": "", "datetime": 1511248746, "fakeid": "3098539049",
                                            "id": 1000000228, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7nUA1AqhxidtpNsgcvvPt-HCyd62Et4AoPIAz0DCnAajetXzE0bCNngLjruTn3c82IFE6nL7Zz99a6japiYvqq0=",
                                               "copyright_stat": 100,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/hp6WA88JQ4R7XrU3tIlicJxC4tIXZpmj9ysZv0F7xQicg8Wkx2gafaJEMH8jBfx4v3zVib63AicDcs9zFs5lqLQNKQ/0?wx_fmt=jpeg",
                                               "del_flag": 1,
                                               "digest": "NumPy 项目宣布将停止支持 Python 2。Python 核心团队已经决定在 2020 年停止支持 Python 2，而 NumPy 项目自 2010 年以来同时支持 Python 2 和 Python 3。",
                                               "fileid": 0, "is_multi": 0, "multi_app_msg_item_list": [],
                                               "source_url": "http://www.solidot.org/story?sid=54514", "subtype": 9,
                                               "title": "开源科学计算包 NumPy 将停止支持 Python 2"},
                          "comm_msg_info": {"content": "", "datetime": 1511140538, "fakeid": "3098539049",
                                            "id": 1000000227, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7mzybvvp4HD1oxLlSHj6qJhuLAQMqxXAl7Q5fmghMc0xPydo7LI*aWI*HvSyFphaNxpD5ny0ZbFlNj2Mds8Vm6I=",
                                               "copyright_stat": 100,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/kOTNkic5gVBEUHe2LMVjYr1wvJQ5YaiapjR7nNDo3iaBPVunDZ3MT7WcnmSmJT2SwsmkeibQSGdleR5Nzzap7OI6fw/0?wx_fmt=jpeg",
                                               "del_flag": 1, "digest": "GitHub 上 10 月份最受欢迎的 10 个开源项目，你用过哪些呢？",
                                               "fileid": 0, "is_multi": 0, "multi_app_msg_item_list": [],
                                               "source_url": "https://www.itcodemonkey.com/article/1132.html",
                                               "subtype": 9, "title": "GitHub 上 10 月份最火的开源项目"},
                          "comm_msg_info": {"content": "", "datetime": 1510890073, "fakeid": "3098539049",
                                            "id": 1000000226, "status": 2, "type": 49}}, {
                          "app_msg_ext_info": {"author": "", "content": "",
                                               "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7vZWHFGA-6Qtx836UnWtpSXUWGEFYidddKOaus8H*shTMHYToMZ83xxmNxg893LARhikgVUa0noICjjFQSasmBw=",
                                               "copyright_stat": 100,
                                               "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/iciaMJDiaNTbG7dOGJ6XxPg6HeTflUjd3nTvFNW3DxDMPd95bKCgL1m2DTKKNxiap3fPict0MpzOiayn9CibMiap32ibjGg/0?wx_fmt=jpeg",
                                               "del_flag": 1, "digest": "股票数据特征分析\n新闻文本分类\n广告销量分析\n房价预测",
                                               "fileid": 504205214, "is_multi": 1, "multi_app_msg_item_list": [
                                  {"author": "dawner", "content": "",
                                   "content_url": "/s?timestamp=1511931536&amp;src=3&amp;ver=1&amp;signature=xys*ZNss1Qe8f*PyTMhk1k-g9nwqdQd5U6klgjz7jLOCRkEKh28V7H-p5WLIMgvWFIOFGnoXQ9Zgg50LClrT7vZWHFGA-6Qtx836UnWtpSVX18biaKVdYyvYr-aGJuuWAAgMXWsCNVR479*6Zd29nTn9V-6KYGcxLKiPPUb1Joo=",
                                   "copyright_stat": 100,
                                   "cover": "http://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38J7cP96dEsaEStHY5baTPRpYyEcALyWicClt1pYm222xSOueg2uYpNtn8YKGFUCExBMZlZnnianiawg/0?wx_fmt=jpeg",
                                   "del_flag": 1,
                                   "digest": "以前在做漏洞Fuzz爬虫时，曾做过URL去重相关的工作，当时是参考了seay法师的文章以及网上零碎的一些资料，感觉做的很简单。近来又遇到相关问题，于是乎有了再次改进算法的念头。",
                                   "fileid": 0,
                                   "source_url": "http://www.freebuf.com/articles/others-articles/151173.html",
                                   "title": "爬虫采集去重优化浅谈"}],
                                               "source_url": "http://pmobile.chinahadoop.cn/ladder-activity/view?id=91&amp;skey=d245affac0c54e46b0fc7f2d69dc38f0",
                                               "subtype": 9, "title": "留给人类的时间不多了？现在不学机器学习更待何时！"},
                          "comm_msg_info": {"content": "", "datetime": 1510794000, "fakeid": "3098539049",
                                            "id": 1000000225, "status": 2, "type": 49}}]}

if __name__ == '__main__':
    print(time_str_format("45分钟前 来自杨树Plus"))
