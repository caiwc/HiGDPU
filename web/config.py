from celery.schedules import timedelta
import tempfile
from kombu import Queue, Exchange
import os
from celery.schedules import crontab

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

WEIBO_NAME = 'HiGDPU'

UPLOAD_PATH = os.path.join(PROJECT_PATH, 'files')

WEIBO_SENT_ERROR = '你的树洞`{content}` 发送失败,请再次编辑后发送.'
WEIBO_COMMENT_MSG = "有人评论了你的树洞: {content}"
WEIBO_REPLY_MSG = "有人回复了你的评论: {content}"
WEIBO_APPLY_DELETE_MSG = "用户申请删除树洞: {content} \n微博id:{id}"
WEIBO_DELETE_MSG = "你的树洞`{content}`因为涉及`{reason}`,被管理员删除"

WEIBO_ONE_HOURS_LIMIT = 5

UNNAMED = "匿名用户"

TOKEN_KEY = "THIRD_SESSION"

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

color_level_dict = {
    0: {'background_color': 'white', 'line_color': '#5a5f75', 'color': 'black'},
    1: {'background_color': 'white', 'line_color': '#fc6e7e', 'color': 'black'},
    2: {'background_color': '#fcffcf', 'line_color': '#3b0f1d', 'color': 'black'},
    3: {'background_color': '#f4e5e6', 'line_color': '#f0df00', 'color': 'black'},
    4: {'background_color': '#f4e5e6', 'line_color': '#f0df00', 'color': 'black'},
    5: {'background_color': '#f4e5e6', 'line_color': '#f0df00', 'color': 'black'}
}


class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'
    RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAEH0GFj7NLg5tGicaoOus7G9Q5Uw"
    RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'
    TOKEN_EXPIRES = 1440 * 365 * 60


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = SQL_URI


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = SQL_URI
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_BACKEND_URL = "redis://localhost:6379/1"

    ALLOWED_EXTENSIONS = {'png', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    REDIS = {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_HOST": "127.0.0.1",
        "CACHE_REDIS_PORT": 6379,
        "CACHE_REDIS_DB": 2,
        "CACHE_REDIS_PASSWORD": "",
    }

    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('send_weibo', Exchange('send_weibo'), routing_key='send_weibo')
    )

    CELERY_DEFAULT_ROUTING_KEY = 'default'

    CELERY_ROUTES = {
        "web.tasks.verifycode_handle": {"queue": "default", "routing_key": "default"},
        "web.tasks.crawl": {"queue": "default", "routing_key": "default"},
        "web.tasks.get_comment_message": {"queue": "default", "routing_key": "default"},
        "web.tasks.add_weibo_tags": {"queue": "default", "routing_key": "default"},
        "web.tasks.multiply": {"queue": "default", "routing_key": "default"},
        "web.tasks.send_weibo": {"queue": "send_weibo", "routing_key": "send_weibo"},
        "web.tasks.send_weibo_comment": {"queue": "send_weibo", "routing_key": "send_weibo"},
        "web.tasks.test": {"queue": "send_weibo", "routing_key": "send_weibo"},
        "web.tasks.weibo_report": {"queue": "default", "routing_key": "default"}

    }

    CELERYBEAT_SCHEDULE = {
        'get_comment_message': {
            'task': 'web.tasks.get_comment_message',
            'schedule': timedelta(hours=4)
        },
        'add_weibo_tags': {
            'task': 'web.tasks.add_weibo_tags',
            'schedule': timedelta(hours=3)
        },
        'weibo_report': {
            'task': 'web.tasks.weibo_report',
            'schedule': crontab(day_of_month=1, hour=0, minute=30)
        }
    }

    CELERY_TIMEZONE = 'Asia/Shanghai'


class TestConfig(DevConfig):
    db_file = tempfile.NamedTemporaryFile()

    DEBUG = True
    DEBUG_TB_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
