from local_settings import Secretid, SecretKey
from QcloudApi.qcloudapi import QcloudApi
import json
import pickle

f = open('/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/my_nlp.pickle', 'rb')
classifier = pickle.load(f)
f.close()


def my(content):
    from nlp import bigrams_words_feature
    item = bigrams_words_feature(content, 5)
    sent = classifier.classify(item)
    print(sent)


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
    my("有需要这些书的吗")