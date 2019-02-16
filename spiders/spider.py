#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()


import requests
from lxml import etree
from domain import Proxy
from utils import request
from utils.log import logger

class ProxySpider(object):
    urls = [] # urls: 抓取代理IP网站的URL列表
    group_xpath = '' # group_xpath: 获取包含IP标签列表的XPATH
    detail_xpath = {} # detail_xpath: 获取IP详情的内部XPATH

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        """
        数据初始
        :param urls: 抓取代理IP网站的URL列表
        :param group_xpath: 获取包含IP标签列表的XPATH
        :param detail_xpath: 获取IP详情的内部XPATH
        """
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        """发送请求, 获取响应数据"""
        response = requests.get(url, headers=request.get_header())
        return response.content

    def get_proxies(self):
        """获取代理IP数据"""
        for url in self.urls:
            try:
                page = self.get_page_from_url(url)
                yield from self.parse_page(page)
            except Exception as ex:
                yield None

    def parse_page(self, page):
        edata = etree.HTML(page)
        rows = edata.xpath(self.group_xpath)
        # 代理列表
        proxy_list = []
        for row in rows:
            try:
                ip = row.xpath(self.detail_xpath['ip'])[0].text.strip()
                port = row.xpath(self.detail_xpath['port'])[0].text.strip()
                area = row.xpath(self.detail_xpath['area'])[0].text.strip()
                proxy =  Proxy(ip, port, area=area)
                proxy_list.append(proxy)
            except Exception as ex:
                logger.exception(ex)
        return proxy_list

if __name__ == '__main__':
    config = {
        'urls':['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 30)],
        'group_xpath': '//table/tr[position()>1]',
        'detail_xpath': {'ip':'./td[1]', 'port':'./td[2]', 'area':'./td[3]'}
    }
    spider = ProxySpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)

