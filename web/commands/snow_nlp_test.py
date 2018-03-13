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
        weibo_list = Weibo.query.filter_by(mode=None).order_by(Weibo.publish_time.desc()).paginate(1, 20).items

        neg_f = open(file_path + '/neg.txt', 'w+')
        pos_f = open(file_path + '/pos.txt', 'w+')
        else_f = open(file_path + '/else.txt', 'w+')

        mode_dict = {
            0: pos_f,
            1: neg_f,
            2: else_f
        }
        for weibo in weibo_list:
            content = weibo.content
            if len(content):
                mode = get_sentitiment(content)
                print(content, mode)
                if mode != 'q' or not mode:
                    write_file = mode_dict[mode]
                    write_file.write(content)
                    write_file.write('\n\n')
                    weibo.mode = mode
                    db.session.add(weibo)
                else:
                    break
        print('finish')
        db.session.commit()
        neg_f.close()
        pos_f.close()
        else_f.close()


config = {
    'Region': 'ap-guangzhou',
    'secretId': Secretid,
    'secretKey': SecretKey,
}
module = "wenzhi"
action = 'TextSentiment'
service = QcloudApi(module, config)


def get_sentitiment(content):
    action_params = {
        'content': content,
        "type": 2
    }
    try:
        res = service.call(action, action_params)
        res = res.decode('utf-8')
        res = json.loads(res)
        print(res)
        pos = res['positive']
        neg = res['negative']
        if pos > neg:
            return 0
        elif pos<neg:
            return 1
        else:
            return 2
    except Exception as e:
        import traceback

        print('traceback.format_exc():\n%s' % traceback.format_exc())


get_sentitiment(content='前几天那个公路驾校组团的还在吗？或者还有人要组团。？？？')
