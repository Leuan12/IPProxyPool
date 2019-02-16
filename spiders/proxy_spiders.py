#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import random

from spiders.spider import ProxySpider
"""
66代理
"""
class Daili66ProxySpider(ProxySpider):
    # 代理URL列表
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 2)]
    # 代理标签列表XPATH
    group_xpath = '//table/tr[position()>1]'
    # 获取代理详情的XPATH
    detail_xpath = {'ip': './td[1]', 'port': './td[2]', 'area': './td[3]'}

from spiders.spider import ProxySpider
"""
西刺代理
"""
class XiciProxiesSpider(ProxySpider):
    urls = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 2)]
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    detail_xpath = {'ip': './td[2]', 'port':'./td[3]', 'area':'./td[4]'}

    def get_page_from_url(self, url):
        time.sleep(random.uniform(1, 10))
        return super().get_page_from_url(url)


"""
ip3366代理
"""

class Ip3366ProxySpider(ProxySpider):
    # 代理URL列表
    urls = ['http://www.ip3366.net/free/?stype={}'.format(i) for i in range(1,5)]
    # 代理标签列表XPATH
    group_xpath = '//table/tbody/tr'
    # 获取代理详情的XPATH
    detail_xpath = {'ip': './td[1]', 'port': './td[2]', 'area': './td[5]'}

"""
ip嗨代理
"""
class IPhaiProxySpider(ProxySpider):
    # 代理URL列表
    urls = ['http://www.iphai.com/free/ng', 'http://www.iphai.com/free/wg']
    # 代理标签列表XPATH
    group_xpath = '//table/tr[position()>1]'
    # 获取代理详情的XPATH
    detail_xpath = {'ip': './td[1]', 'port': './td[2]', 'area': './td[5]'}

"""
proxylistplus代理
"""
class ProxylistplusSpider(ProxySpider):
    # 代理URL列表
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    # 代理标签列表XPATH
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>3]'
    # 获取代理详情的XPATH
    detail_xpath = {'ip': './td[2]', 'port': './td[3]', 'area': './td[5]'}

"""
goubanjia代理
"""
class ProxylistplusSpider(ProxySpider):
    # 代理URL列表
    urls = ['http://www.goubanjia.com/']
    # 代理标签列表XPATH
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>3]'
    # 获取代理详情的XPATH
    detail_xpath = {'ip': './td[2]', 'port': './td[3]', 'area': './td[5]'}

if __name__ == '__main__':
    spider = ProxylistplusSpider()
    for proxy in spider.get_proxies():
        print(proxy)