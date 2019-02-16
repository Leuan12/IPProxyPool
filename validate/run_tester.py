#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool

from queue import Queue
from db.mongo_pool import MongoPool
from validate import validator
from utils.log import logger
import settings
import schedule
import time

'''
代理检测者
'''
class RunTester(object):
    def __init__(self):
        self.queue = Queue()
        self.running = False
        self.proxyPool = MongoPool() # 代理池
        self.pool = Pool() # 代理池

    def _test_proxy(self):
        # 从代理队列中, 获取请求
        proxy = self.queue.get()
        # 验证当前的代理
        try:
            proxy = validator.check_proxy(proxy)
            # 如果速度为-1就说明请求失败了
            if proxy.speed == -1:
                # 如果分数为0, 就删除该代理
                if proxy.score != 0:
                    self.proxyPool.decrease_score(proxy)
                else:
                    self.proxyPool.delete(proxy)
                    logger.info('删除代理:{}'.format(proxy))
            else:
                # 如果请求成功了, 恢复分数
                self.proxyPool.resume_score(proxy)
        except Exception as ex:
            logger.error('检查代理错误')
            logger.exception(ex)

        self.queue.task_done()

    def _test_proxy_finish(self, temp):
        self.pool.apply_async(self._test_proxy, callback=self._test_proxy_finish)

    def run(self):
        proxies = self.proxyPool.all()
        if proxies is None or len(proxies) == 0:
            print("代理池为空")
            return

        self.running = True

        # 获取所有的代理
        for proxy in proxies:
            self.queue.put(proxy)

        # 开启多个异步任务执行检查IP的任务
        for i in range(settings.TESTER_ANSYC_COUNT):
            self.pool.apply_async(self._test_proxy,callback=self._test_proxy_finish)

        self.queue.join()

    @staticmethod
    def start():
        tester = RunTester()
        tester.run()

if __name__ == '__main__':
    # 每隔2小时检查下代理是否可用
    schedule.every(1).minutes.do(RunTester.start)
    while True:
        schedule.run_pending()
        time.sleep(1)

