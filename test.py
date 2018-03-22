import json
import pickle

from QcloudApi.qcloudapi import QcloudApi

from local_settings import Secretid, SecretKey

f = open('/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/my_nlp2.pickle', 'rb')
classifier = pickle.load(f)
f.close()


def my(content):
    from weibo_nlp.nlp import bigrams_words_feature
    import jieba
    item = bigrams_words_feature(jieba.cut(content, cut_all=False), 10)
    sent1 = classifier.prob_classify(item)
    prob = sent1._prob_dict
    print(sent1.max())
    print('pos:', prob['pos'], 'neg:', prob['neg'])


def qclud(content):
    config = {
        'Region': 'ap-guangzhou',
        'secretId': Secretid,
        'secretKey': SecretKey,
    }

    module = "wenzhi"

    action = 'TextClassify'

    action_params = {
        'content': content,
    }

    try:
        service = QcloudApi(module, config)
        # print(service.generateUrl(action, action_params))
        res = service.call(action, action_params)
        res = res.decode('utf-8')
        res = json.loads(res)
        print(res)
    except Exception as e:
        import traceback

        print('traceback.format_exc():\n%s' % traceback.format_exc())


def baidu(content):
    from aip import AipNlp
    APP_ID = '10922374'
    API_KEY = 'DIGhcSxzbOyOIqaUUaGMLV5O'
    SECRET_KEY = '0hMz3H7uiSwtpprvuyWs6ybtPhy6Lwdk'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    print(client.sentimentClassify(text=content))


if __name__ == '__main__':
    my("半圆广场搞活动的放歌要放就放好听点 别一会放停一会，真的很扰民 ")