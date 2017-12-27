from selenium import webdriver
from qyweixin import qyweixin_api
import time
from weixin_scrapy.settings import PHANTOMJS_PATH


def handel_verifycode(url, operation='weixin'):
    driver = webdriver.PhantomJS(PHANTOMJS_PATH)
    # driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)
    driver.get_screenshot_as_file("/tmp/HiGDPU/index.png")
    media_id = qyweixin_api.upload_media(qyweixin_api.qyweixin_img_type, "/tmp/HiGDPU/index.png")
    qyweixin_api.send_weixin_message(qyweixin_api.qyweixin_img_type, {'media_id': media_id})
    code = input('验证码:')
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
            driver.find_element_by_css_selector('#sogou_vr_11002301_box_0 .gzh-box2 .txt-box .tit a').click()
            time.sleep(2)
        except:
            pass
    driver.quit()


if __name__ == '__main__':
    url = input("url:")
    operation = input("operation:")
    handel_verifycode(url=url, operation=operation)
