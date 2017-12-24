import requests

url = 'https://mp.weixin.qq.com/profile?src=3&timestamp=1512893728&ver=1&signature=bU7cJGnuyhI-I-QJkL*5sVUOozL0vuuSAMUbimJ8oGyQu1lIgCfH-56hYhH7uugflM7JGRXStzlHNMntp88h-w=='

ip_url = 'http://icanhazip.com/'

gzh_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Host': 'mp.weixin.qq.com',

}

proxies = {
    "http": "http://93.167.224.213:80",
    # "https": "http://221.7.255.168:80",
}

html = requests.get(url=ip_url, headers=gzh_headers, proxies=proxies)
print(html.text,html.status_code)
