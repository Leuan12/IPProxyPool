import requests
import time
import json
from utils import request
import settings
from domain import Proxy
from utils.log import logger

def check_proxy(proxy):
    '''
    检测代理协议类型, 匿名程度
    :param
    :return:(协议: http和https:2,https:1,http:0, 匿名程度:高匿:0,匿名: 1, 透明:0 , 速度, 单位s )
    '''

    # 根据proxy对象构造, 请求使用的代理
    proxies = {
        'http': "http://{}:{}".format(proxy.ip, proxy.port),
        'https':"https://{}:{}".format(proxy.ip, proxy.port),
    }

    protocol = -1 # 协议
    nick_types = -1 # 匿名类型
    speed = -1 # 速度
    http, http_types, http_speed = _check_http_proxy(proxies)
    https, https_types, https_speed = _check_http_proxy(proxies, False)
    if http and https:

        proxy.protocol = 2
        proxy.nick_type = http_types
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_types
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_types
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1

    logger.debug(proxy)
    return proxy


def _check_http_proxy(proxies, isHttp=True):
    types = -1
    speed = -1
    if isHttp:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    try:
        start = time.time()
        r = requests.get(url=test_url, headers=request.get_header(), timeout=settings.TIMEOUT, proxies=proxies)
        if r.ok:
            speed = round(time.time() - start, 2)
            content = json.loads(r.text)
            headers = content['headers']
            ip = content['origin']
            proxy_connection = headers.get('Proxy-Connection', None)
            if ',' in ip:
                types = 2 # 透明
            elif proxy_connection:
                types = 1 # 匿名
            else:
                types = 0 # 高匿
            return True, types, speed
        else:
            return False, types, speed
    except Exception as e:
        return False, types, speed

if __name__ == '__main__':
    proxy = Proxy('118.190.95.35', '9001')
    rs = check_proxy(proxy)
    print(proxy.protocol)
    print(rs)
