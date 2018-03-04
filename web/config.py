from celery.schedules import crontab
from kombu import Queue, Exchange
import os

WEB_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.dirname(WEB_PATH)
if os.path.exists(os.path.join(os.path.dirname(WEB_PATH), 'local_settings.py')):
    from local_settings import *

SQL_URI = 'mysql://{user}:{password}@{host}:{port}/{dbname}'.format(user=MYSQL_USER,
                                                                    host=MYSQL_HOST,
                                                                    password=MYSQL_PASSWORD,
                                                                    port=MYSQL_PORT,
                                                                    dbname=MYSQL_DBNAME)

WEIXIN_AUTH_URL = "https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code".format(
    APPID=WEIXIN_APPID, SECRET=WEIXIN_SECRET, JSCODE='{JSCODE}')

APP_KEY = APP_KEY
APP_SECRET = APP_SECRET
CALLBACK_URL = CALLBACK_URL

QYWEIXIN_VERIFYCODE = '识别验证码'


class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'
    RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAEH0GFj7NLg5tGicaoOus7G9Q5Uw"
    RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'
    TOKEN_EXPIRES = 1440 * 31 * 60


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = SQL_URI


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = SQL_URI
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_BACKEND_URL = "redis://localhost:6379/1"

    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('send_weibo', Exchange('send_weibo'), routing_key='send_weibo')
    )

    CELERY_ROUTES = {
        "web.tasks.verifycode_handle":{"queue": "default", "routing_key": "default"},
        "web.tasks.crawl":{"queue": "default", "routing_key": "default"},
        "web.tasks.multiply":{"queue": "default", "routing_key": "default"},
        "web.tasks.send_weibo": {"queue": "send_weibo", "routing_key": "send_weibo"},
    }

    CELERYBEAT_SCHEDULE = {
        'weekly-digest': {
            'task': 'tasks.digest',
            'schedule': crontab(day_of_week=6, hour='10')
        },
    }
