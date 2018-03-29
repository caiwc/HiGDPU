import matplotlib

matplotlib.use('Agg')

import datetime
from qyweixin.qyweixin_api import send_weixin_message, upload_media, qyweixin_img_type
from os import path
from web.models import Weibo, Tag, db
from matplotlib.pyplot import plot, savefig
import matplotlib.font_manager as mfm
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import numpy as np

d = path.dirname(__file__)
today = datetime.date.today()
font_path = path.join(d, 'Chinese.ttf')
prop = mfm.FontProperties(fname=font_path)


def zs_dxc_count(weibo_query):
    # 获取带有大学城和中山标签的树洞数量,调用get_pic生成饼状图
    zs_weibo_count = weibo_query.filter(Weibo.tags.any(Tag.name == '中山')).count()
    dxc_weibo_count = weibo_query.filter(Weibo.tags.any(Tag.name == '大学城')).count()
    weibo_publish_time = weibo_query.first().publish_time
    get_pic(data=[zs_weibo_count, dxc_weibo_count], index=['中山', '大学城'], kind='pie', title='中山-大学城发送数量对比',
            year=weibo_publish_time.year, month=weibo_publish_time.month)
    return zs_weibo_count, dxc_weibo_count


def daily_weibo_count(weibo_query):
    # 遍历周期内全部树洞, 记录每条树洞发布时间和日期.
    daily_count = {}  # daily_count 记录了周期内一天24小时每小时树洞的数量
    data_array = []  # data_array 记录每条树洞小时数和日期数,生成一个多维数组
    for weibo in weibo_query.all():
        hour = weibo.publish_time.hour
        minute = weibo.publish_time.minute
        float_hour = float(hour) + minute / 60
        day = weibo.publish_time.day
        data_array.append([float_hour, day])
        if hour not in daily_count:
            daily_count[hour] = 0
        else:
            daily_count[hour] += 1
    sorted(daily_count)
    #  用daily_count生成当月每小时数量统计折线图
    weibo = weibo_query.first()
    year = weibo.publish_time.year
    month = weibo.publish_time.month
    get_pic(data=list(daily_count.values()), index=list(daily_count.keys()), kind='basic', title='当月每小时数量统计',
            year=year, month=month, x_name='hours', y_name='count')

    # 用data_array生成全月树洞发布散点图
    get_pic(data=data_array, kind='scatter', title='全月树洞发布散点图', year=year, month=month,
            y_max=today.day + 1)


def _get_year_month(now, n=0):
    '''
    获取年 月
    :param n: n个月前
    :return:
    '''
    thisyear = now.year
    thismon = now.month

    year = thisyear - int(n / 12)
    n = n % 12
    if n >= thismon:
        year -= 1
        n -= thismon
        thismon = 12
    thismon -= n
    return year, thismon


def recently_weibo_count(month_ago, year=None, month=None):
    from sqlalchemy import extract, func
    if not year and not month:
        end_date = today
    else:
        if month == 12:
            end_date = datetime.date(year=year, month=month, day=31)
        else:
            end_date = datetime.date(year=year, month=month + 1, day=1) - datetime.timedelta(days=1)
    year, month = _get_year_month(end_date, month_ago)  # 获取几个月前的年份与月份
    month_ago_date = datetime.date(year, month, 1)
    weibo_query = db.session.query(extract('month', Weibo.publish_time).label('month'),
                                   func.count('*').label('count')).filter(
        Weibo.publish_time.between(month_ago_date, end_date)).group_by('month').all()
    month_list = []
    while len(month_list) <= month_ago:
        month_list.append(month)
        month += 1
        if month > 12:
            month = month % 12
    res = []
    index = []
    for m in month_list:
        for weibo in weibo_query:
            if weibo.month == m:
                index.append(weibo[0])
                res.append(weibo[1])
    get_pic(data=res, index=index, kind='bar', title='近几月树洞统计', year=end_date.year, month=end_date.month, x_name='月份',
            y_name='数量')


def get_pic(data, kind, title, year, month, index=None, x_name=None, y_name=None, y_max=None):
    # 使用python的pandas和matplotlib生成统计图片
    plt.clf()
    if kind == 'bar':
        s = Series(data, index=index, name='树洞数量')
        s.plot(kind=kind, color='c', alpha=0.6, stacked=True)
        plt.xlabel(x_name, fontproperties=prop)
        plt.ylabel(y_name, fontproperties=prop)
        plt.legend(prop=prop)
    elif kind == 'pie':
        s = Series(data=data, index=[' ', ' '], name='')
        s.plot.pie(figsize=(6, 6), colors={'g', 'c'})
        plt.legend(index, prop=prop)
    elif kind == 'basic':
        s = Series(data=data, index=index, name='树洞数量')
        s.plot(color='c', marker='o', alpha=0.6, stacked=True)
        plt.xlabel(x_name, fontproperties=prop)
        plt.ylabel(y_name, fontproperties=prop)
        plt.xticks(np.arange(0, 25, 2))
        # plt.yticks(np.arange(0, max(data) + 1, 2))
        plt.legend(prop=prop)
    elif kind == 'scatter':
        df = DataFrame(np.array(data), columns=['hour', 'day'])
        df.plot.scatter(x='hour', y='day')
        plt.xticks(np.arange(0, 25, 2))
        plt.yticks(np.arange(1, y_max + 1, 2))
    plt.title(title, fontproperties=prop)

    file_name = "{}_{}_{}.jpg".format(kind, year, month)
    # 保存图片
    save_path = path.join(path.dirname(d), 'web/static', file_name)
    savefig(save_path)
    # 将生成的图片发送至企业微信,汇报给管理员
    media_id = upload_media(file_type=qyweixin_img_type, file_path=save_path)
    send_weixin_message(qyweixin_img_type, {'media_id': media_id})
