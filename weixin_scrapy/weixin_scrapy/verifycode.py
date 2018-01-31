from selenium import webdriver
from qyweixin import qyweixin_api
import time
from web.utils import timeoutFn
from weixin_scrapy.settings import PHANTOMJS_PATH
import redis


def handel_verifycode(url, operation='weixin', by_qyweixin=False):
    if len(PHANTOMJS_PATH) > 0:
        driver = webdriver.PhantomJS(PHANTOMJS_PATH)
    else:
        driver = webdriver.PhantomJS()
    # driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)
    driver.get_screenshot_as_file("/tmp/HiGDPU/index.png")
    media_id = qyweixin_api.upload_media(qyweixin_api.qyweixin_img_type, "/tmp/HiGDPU/index.png")
    qyweixin_api.send_weixin_message(qyweixin_api.qyweixin_img_type, {'media_id': media_id})
    code = timeoutFn(get_code, kwargs={'by_qyweixin': by_qyweixin}, timeout_duration=20, default=None)
    if code:
        if operation == 'weixin':
            driver.find_element_by_id('input').send_keys(code)
            driver.find_element_by_id('bt').click()
        elif operation == 'sougou':
            driver.find_element_by_id('seccodeInput').send_keys(code)
            driver.find_element_by_id('submit').click()
        time.sleep(3)
        driver.get_screenshot_as_file("/tmp/HiGDPU/success.png")
        s_media_id = qyweixin_api.upload_media(qyweixin_api.qyweixin_img_type, "/tmp/HiGDPU/success.png")
        qyweixin_api.send_weixin_message(qyweixin_api.qyweixin_img_type, {'media_id': s_media_id})
        if operation == 'sougou':
            try:
                driver.find_element_by_xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a').click()
                time.sleep(2)
                driver.get_screenshot_as_file("/tmp/HiGDPU/success.png")
                s_media_id = qyweixin_api.upload_media(qyweixin_api.qyweixin_img_type, "/tmp/HiGDPU/success.png")
                qyweixin_api.send_weixin_message(qyweixin_api.qyweixin_img_type, {'media_id': s_media_id})
            except:
                pass
    driver.quit()
    return True


def get_code(by_qyweixin):
    if not by_qyweixin:
        code = input('输入验证码')
        return code
    else:
        r = redis.Redis(host='localhost', port=6379, db=0)
        for i in range(20):
            try:
                a = r.get('code')
                if a:
                    print('success to get code')
                    return a
                else:
                    time.sleep(1)
                    print('fail to get code,count {}'.format(i + 1))
            except:
                print('fail to get code,count {}'.format(i+1))
        return None


if __name__ == '__main__':
    url = input("url:")
    operation = input("operation:")
    handel_verifycode(url=url, operation=operation)
