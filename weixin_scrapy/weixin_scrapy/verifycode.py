import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from selenium import webdriver
from qyweixin import qyweixin_api
import time
from weixin_scrapy.weixin_scrapy.settings import PHANTOMJS_PATH

def handel_verifcode(url=None):
    driver = webdriver.PhantomJS(PHANTOMJS_PATH)
    # driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.maximize_window()
    if not url:
        url = "http://mp.weixin.qq.com/profile?src=3&timestamp=1513734748&ver=1&signature=yM34HJn9jtn4FkjSiHuQuMGOlPjI5jMquEWHDSiRcbiJk837*vgx*RkPuz*bnka1rc8I7S*yoarZ8QK8eq9eAA=="
    driver.get(url)
    time.sleep(2)

    driver.get_screenshot_as_file("/tmp/HiGDPU/index.png")
    media_id = qyweixin_api.upload_media(qyweixin_api.qyweixin_img_type,"/tmp/HiGDPU/index.png")
    qyweixin_api.send_weixin_message(qyweixin_api.qyweixin_img_type, {'media_id': media_id})
    code = input('验证码:')
    driver.find_element_by_id('input').send_keys(code)
    driver.find_element_by_id('bt').click()
    time.sleep(3)
    driver.quit()

if __name__ == '__main__':
    handel_verifcode()