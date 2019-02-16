#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from db.mongo_pool import MongoPool
from domain import Proxy

import json

class ProxyApi(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.proxyPool = MongoPool()

        @self.app.route('/proxies/<protocol>')
        def all(protocol='http'):
            lis = []
            for proxy in self.proxyPool.all(protocol):
                lis.append(proxy.dict)
            return json.dumps(lis)

        @self.app.route('/proxies/random/<protocol>')
        def random(protocol='http'):
            print(protocol)
            proxy = self.proxyPool.random(protocol)
            return '{}://{}:{}'.format(protocol, proxy.ip, proxy.port)

        @self.app.route('/decrease_score/<ip>')
        def decrease_score(ip=''):
            proxy = Proxy(ip=ip)
            return self.proxyPool.decrease_score(proxy)

    def run(self):
        self.app.run(host="0.0.0.0",port=6868)

    @classmethod
    def start(cls):
        proxy_api = cls()
        proxy_api.run()

if __name__ == '__main__':
    proxy_api = ProxyApi()
    proxy_api.run()