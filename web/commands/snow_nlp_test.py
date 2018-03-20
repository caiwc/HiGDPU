from weixin_scrapy.settings import PROJECT_PATH
from flask_script import Manager, Command
import os
from web.models import db, Weibo
from local_settings import Secretid, SecretKey
from QcloudApi.qcloudapi import QcloudApi
import json

file_path = os.path.join(PROJECT_PATH, 'weibo_nlp')


class Classify(Command):
    def run(self):
        weibo_list = Weibo.query.filter_by(mode=None).order_by(Weibo.publish_time.desc()).paginate(1, 10).items
        for weibo in weibo_list:
            content = weibo.content
            if len(content.strip()) > 0:
                try:
                    # mode_1, pos1, neg1 = get_baidu_sentitiment(content.strip('\u200b'))
                    # mode_2, pos2, neg2 = get_qlcloud_sentitiment(content)
                    # if mode_1 == mode_2:
                    #     mode = mode_1
                    # else:
                    #     # pos_max = max(pos1, pos2)
                    #     # neg_max = max(neg1, neg2)
                    #     # mode = 0 if pos_max > neg_max else 1
                    #     mode = 2
                    mode = boson(content)
                    print(content, mode)
                    if mode != 'q' or not mode:

                        weibo.mode = mode
                        db.session.add(weibo)
                    else:
                        break

                except Exception as e:
                    print(content)
                    print(e)

        db.session.commit()
        print('finish')


config = {
    'Region': 'ap-guangzhou',
    'secretId': Secretid,
    'secretKey': SecretKey,
}
module = "wenzhi"
action = 'TextSentiment'


def get_qlcloud_sentitiment(content):
    action_params = {
        'content': content,
        "type": 4
    }
    service = QcloudApi(module, config)
    try:

        res = service.call(action, action_params)
        res = res.decode('utf-8')
        res = json.loads(res)
        print(res)
        pos = res['positive']
        neg = res['negative']
        if pos > neg:
            return 0, pos, neg
        elif pos < neg:
            return 1, pos, neg
        else:
            return 2, pos, neg
    except Exception as e:
        import traceback

        print('traceback.format_exc():\n%s' % traceback.format_exc())


from aip import AipNlp

APP_ID = '10922374'
API_KEY = 'DIGhcSxzbOyOIqaUUaGMLV5O'
SECRET_KEY = '0hMz3H7uiSwtpprvuyWs6ybtPhy6Lwdk'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def get_baidu_sentitiment(content):
    res = client.sentimentClassify(text=content)
    res = res['items'][0]
    mode = res['sentiment']
    print(res)
    pos = res['positive_prob']
    neg = res['negative_prob']
    if res['confidence'] > 0.4:
        if mode == 0:
            return 1, pos, neg
        elif mode == 1:
            return 2, pos, neg
        else:
            return 0, pos, neg
    else:
        return 2, pos, neg


def boson(content):
    from bosonnlp import BosonNLP
    nlp = BosonNLP('o65Fe84P.24500.MrugM8rSFa7A')
    resp = nlp.sentiment(content, model='weibo')
    res = resp[0]
    print(res)
    if res[0] - res[1] > 0.5:
        return 0
    elif res[1] - res[0] > 0.5:
        return 1
    else:
        return 2
