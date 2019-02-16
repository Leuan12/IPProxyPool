#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import importlib

import settings
from validate.validator import check_proxy
from db.mongo_pool import MongoPool
from utils.log import logger
import schedule
import time

class RunSpider(object):
    def __init__(self):
        self.coroutine_pool = Pool()
        self.proxy_pool = MongoPool()

    def _auto_import_instances(self, paths=[]):
        """根据配置信息, 自动导入爬虫"""
        instances = []
        for path in paths:
            # print(path)
            module_name, cls_name = path.rsplit('.', maxsplit=1)
            module = importlib.import_module(module_name)
            cls = getattr(module, cls_name)
            instances.append(cls())
        return instances

    # 处理代理
    def process_proxy_spiders(self):
        # 获取代理爬虫
        spiders = self._auto_import_instances(settings.PROXIES_SPIDERS)

        # 执行爬虫获取代理
        for spider in spiders:
            print(spider)
            # 使用异步来执行爬虫任务
            # 好处: 1. 避免一个爬虫出错后, 后面的爬虫无法执行, 2. 提高爬取的速度
            self.coroutine_pool.apply_async(self._process_one_spider, args=(spider, ))

        # 等待所有爬虫任务执行完成
        self.coroutine_pool.join()

    def _process_one_spider(self, spider):
        try:
            proxies = spider.get_proxies()
            if proxies is None:
                # 如果获取代理是None, 直接返回.
                return

            for proxy in proxies:
                if proxy is None:
                    # 如果是None继续一个
                    continue
                # 检查代理, 获取代理协议类型, 匿名程度, 和速度
                proxy = check_proxy(proxy)
                # 如果代理速度不为-1, 就是说明该代理可用
                if proxy.speed != -1:
                    # 保存该代理到数据库中
                    self.proxy_pool.insert(proxy)
                    logger.info('新代理IP: {} 入库'.format(proxy))

        except Exception as e:
            logger.exception(e)
            logger.exception("爬虫{} 出现错误".format(spider))

    def run(self):
        self.process_proxy_spiders()

    @classmethod
    def start(cls):
        spider = cls()
        spider.run()


if __name__ == '__main__':
    # 先执行一下
    RunSpider.main()
    # 每隔30个小时, 开始爬下新的IP
    schedule.every(2).hours.do(RunSpider.start())
    while True:
        schedule.run_pending()
        time.sleep(1)

