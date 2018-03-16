import local_settings as settings
from requests_toolbelt import MultipartEncoder
import requests
import time

qyweixin_img_type = 'image'
qyweixin_text_type = 'text'


def do_weixin_api(method, url, headers=None, data=None, j_data=None, params=None, files=None):
    if not headers:
        headers = {
            'content-type': 'application/json',
        }

    try:
        res = requests.request(method=method, headers=headers, url=url, params=params, data=data, json=j_data)
        print(method, res.url, data)
    except Exception as e:
        print('请求失败', method, url, params, data, e)
        return False, str(e)

    print('weixin res: ', res.content)

    if res.status_code != 200:
        try:
            return False, res.json()['errmsg']
        except Exception as e:
            print(method, res.url, data, e, res.content)
            return False, str(e)
    else:
        try:
            js = res.json()
            if js['errcode'] != 0:
                print('请求失败 ', js['errmsg'], res.url, data)
                return False, js['errmsg']
        except Exception as e:
            print(method, res.url, data, e, res.content)
            return False, str(e)

    return True, js


def get_access_token():
    payload = {
        'corpid': settings.CORPID,
        'corpsecret': settings.CORPSERCET
    }
    url = settings.GET_TOKEN_URL
    flag, res = do_weixin_api(method='GET', url=url, params=payload)
    token = None
    if flag:
        token = res.get('access_token', None)
    if token:
        return token
    else:
        raise ValueError('get token error')


def upload_media(file_type, file_path):
    token = get_access_token()
    payload = {
        'access_token': token,
        'type': file_type
    }
    m = MultipartEncoder(
        fields={
            'field2': ('filename', open(file_path, 'rb'), 'text/plain')
        })
    print(m.content_type)
    url = settings.MEIDA_UPLOAD
    flag, res = do_weixin_api(method='POST', url=url, headers={'Content-Type': m.content_type}, data=m, params=payload)
    if flag:
        return res['media_id']
    else:
        return ValueError(res)


token = None
get_token_time = None


def send_weixin_message(send_type, msg_content, to_list=None):
    if not to_list:
        to_list = settings.USER_LIST
    url = settings.SEND_MESSAGE_URL
    global token, get_token_time
    if token and get_token_time and time.time() - get_token_time < 7200:
        pass
    else:
        get_token_time = time.time()
        token = get_access_token()

    payload = {'access_token': token}
    send_data = {
        "touser": "|".join(to_list),
        "toparty": "",
        "totag": "",
        "agentid": settings.AGENTID,
        "msgtype": send_type
    }
    if send_type == qyweixin_img_type:
        media_id = msg_content['media_id']
        send_data.update({
            "image": {
                "media_id": media_id
            },
        })
    if send_type == qyweixin_text_type:
        send_data.update({
            "text": {
                "content": msg_content
            },
        })
    flag, res = do_weixin_api('POST', url, j_data=send_data, params=payload)
    if not flag:
        raise ValueError(res)


if __name__ == '__main__':
    # upload_media('image', '/tmp/HiGDPU/index.png')
    send_weixin_message(qyweixin_text_type,"test")
