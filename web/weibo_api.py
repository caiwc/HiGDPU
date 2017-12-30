# -*- coding: utf-8 -*-

'''
Python3 client SDK for sina weibo API using OAuth 2.
'''

import time
import requests
from requests_toolbelt import MultipartEncoder
from urllib.parse import quote


def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.items():
        o[str(k)] = v
    return o


class APIError(Exception):
    '''
    raise APIError if got failed json message.
    '''

    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        Exception.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)


class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


def _encode_params(**kw):
    '''
    Encode parameters.
    '''
    args = []
    for k, v in kw.items():
        qv = v.encode('utf-8') if isinstance(v, str) else str(v)
        args.append('%s=%s' % (k, quote(qv)))
    return '&'.join(args)


def _encode_data(**kw):
    '''
    Encode data.
    '''
    data = {}
    for k, v in kw.items():
        qv = v.encode('utf-8') if isinstance(v, str) else str(v)
        data.update({k: qv})
    return data


def _encode_multipart(**kw):
    '''
    Build a multipart/form-data body with generated random boundary.
    '''
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.items():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            filename = getattr(v, 'name', '')
            n = filename.rfind('.')
            ext = filename[n:].lower() if n != (-1) else ""
            content = v.read()
            content = content.decode('ISO-8859-1')
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v if isinstance(v, str) else v.decode('utf-8'))
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary


_CONTENT_TYPES = {'.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                  '.jpe': 'image/jpeg'}


def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')


_HTTP_GET = 'GET'
_HTTP_POST = 'POST'
_HTTP_UPLOAD = 'POST'


def _http_call(url, method, authorization=None, params=None, data=None, files=None):
    '''
    send an http request and expect to return a json object if no error.
    '''
    headers = {}
    if files:
        data.update(files)
        data = MultipartEncoder(
            fields=data)
    if authorization:
        headers.update({'Authorization': 'OAuth2 %s' % authorization})
    if files:
        headers.update({'Content-Type': data.content_type})
    res = requests.request(method=method, headers=headers, url=url, data=data, params=params)
    r = res.json()
    if 'error_code' in r:
        print(r)
        raise APIError(r['error_code'], r['error_description'], r['request'])
    return r


class HttpObject(object):
    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            if self.client.is_expires():
                raise APIError('21327', 'expired_token', attr)
            return _http_call('%s%s.json' % (self.client.api_url, attr.replace('__', '/')), self.method,
                              self.client.access_token, **kw)

        return wrap


class APIClient(object):
    '''
    API client using synchronized invocation.
    '''

    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='api.weibo.com',
                 version='2'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'https://%s/oauth2/' % domain
        self.api_url = 'https://%s/%s/' % (domain, version)
        self.access_token = None
        self.expires = 0.0
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def set_access_token(self, access_token, expires_in):
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def get_authorize_url(self, redirect_uri=None, display='default'):
        '''
        return the authroize url that should be redirect.
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        return '%s%s?%s' % (self.auth_url, 'authorize',
                            _encode_params(client_id=self.client_id,
                                           response_type='code',
                                           display=display,
                                           redirect_uri=redirect))

    def request_access_token(self, code, redirect_uri=None):
        '''
        return access token as object: {"access_token":"your-access-token","expires_in":12345678}, expires_in is standard unix-epoch-time
        '''

        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')

        r = _http_call(url='%s%s' % (self.auth_url, 'access_token'), method=_HTTP_POST,
                       data={'client_id': self.client_id,
                             'client_secret': self.client_secret,
                             'redirect_uri': redirect,
                             'code': code,
                             'grant_type': 'authorization_code'})

        r['expires_in'] += int(time.time())
        return r

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)


def post_weibo(client, content, files_path=None):
    if not isinstance(client, APIClient):
        raise APIError('00001', 'client type error', 'OAuth2 request')
    data = {
        'status': content
    }
    try:
        if files_path:
            return client.upload.statuses__share(data=data, files={'filename', open(files_path, 'rb'),
                                                                   'text/plain'})
        else:
            return client.post.statuses__share(data=data)
    except Exception as e:
        print(e)


def get_weibo(client, page_size=5, page=1):
    params = {'screen_name': 'HiGDPU', 'count': page_size, 'page': page}
    return client.get.statuses__user_timeline(params=params)


def get_weibo_detial(client, weibo_id):
    params = {'id': weibo_id}
    return client.get.statuses__show(params=params)


def get_emotions(client, e_type='普通表情', lang='cnname'):
    emotions_dict = {
        '普通表情': 'face',
        '魔法表情': 'ani',
        '动漫表情': 'cartoon'
    }
    params = {'type': emotions_dict[e_type], 'language': lang}
    return client.get.emotions(params=params)


def get_weibo_comment(client, weibo_id):
    params = {
        'id': weibo_id,
    }
    res = client.get.comments__show(params=params)
    return res['comments']


def post_weibo_commet(client, weibo_id, comment):
    data = {'id': weibo_id, 'comment': comment}
    res = client.post.comments__create(data=data)
    return res


def get_client():
    APP_KEY = "1821462258"
    APP_SECRET = "3111564bdae15d624c52e19a1449073c"
    CALLBACK_URL = 'https://weibo.com/HiGDPU'
    # step 2 引导用户到授权地址
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    return client


def main():
    try:
        # step 1 定义 app key，app secret，回调地址：
        client = get_client()
        # client.access_token = '2.00KTSG6CWXfQzB4432cee7e0253_yC'
        # client.expires = 1514560111
        print(client.get_authorize_url())
        # step 3 换取Access Token
        r = client.request_access_token(input("Input code:"))  # 输入授权地址中获得的CODE
        client.set_access_token(r['access_token'], r['expires_in'])
        print(r['expires_in'])
        print(r['access_token'])
        # # step 4 使用获得的OAuth2.0 Access Token调用API
        # print(client.get.account__get_uid())
        # print(client.post.statuses__share(data={'access_token': r['access_token'],
        #                                         'status': '测试Python3 + OAuth 2.0发微博 ' + str(
        #                                             time.time()) + 'https://weibo.com/HiGDPU'}))
        print(client.upload.statuses__share(data={
            'status': '测试Python3 + OAuth 2.0发微博 ' + str(
                time.time()) + 'https://weibo.com/HiGDPU'},
            files={'pic': (
                'filename', open('/Users/caiweicheng/Desktop/test.jpg', 'rb'),
                'text/plain')}))

    except Exception as pyOauth2Error:
        print(str(pyOauth2Error))


if __name__ == '__main__':
    # main()
    client = get_client()
    client.access_token = '2.00KTSG6CWXfQzB4432cee7e0253_yC'
    client.expires = 1514560111
    res = get_weibo_comment(client, 4190310256614338)
    print(res)
