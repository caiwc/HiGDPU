import unittest

from web import create_app
from web.models import db, User
from web.extensions import rest_api


class TestURLs(unittest.TestCase):
    def setUp(self):
        # Bug workarounds

        rest_api.resources = []

        app = create_app('web.config.TestConfig')
        self.client = app.test_client()

        # Bug workaround
        db.app = app

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_redirect(self):
        """ Tests if the root URL gives a 302 """

        result = self.client.get('/')
        self.assertEqual(result.status_code, 302)
        self.assertIn("/blog/", result.headers['Location'])

    def test_weixin(self):
        """ Tests if the weixin api returns successfully """

        result = self.client.get('http://127.0.0.1:5000/api/weixin')
        self.assertEqual(result.status_code, 200)

    def test_weibo(self):
        result = self.client.get('http://127.0.0.1:5000/api/weibo')
        self.assertEqual(result.status_code, 200)

    def test_search(self):
        result = self.client.post('/api/search', data=dict(query='你', page=1))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data), 2)

    def test_weibo_post(self):
        """ Tests if the weibo post correctly """
        import datetime
        test_user = User()
        test_user.openid = "test_id"
        test_user.session_key = "test"
        test_user.third_session = "test"
        test_user.expires_in = datetime.datetime.now()
        db.session.add(test_user)
        db.session.commit()

        result = self.client.post('/api/weibo/', data=dict(
            content='test,test'
        ), headers={'third-session': 'test_id'}, follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('发送成功,谢谢使用', result.data)


if __name__ == '__main__':
    unittest.main()
