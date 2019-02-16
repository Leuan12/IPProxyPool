import schedule
import time
from multiprocessing import Process

from spiders.run_spiders import RunSpider
from validate.run_tester import RunTester
from api.proxy_api import ProxyApi
import settings


def run_spider():
    # 启动先运行一下
    RunSpider.start()
    # 每隔 SPIDER_INTERVAL 小时检查下代理是否可用
    schedule.every(settings.SPIDER_INTERVAL).hours.do(RunSpider.start)
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_tester():
    # 启动先运行下
    RunTester.start()

    # 每隔TESTER_INTERVAL分钟检查下代理是否可用
    schedule.every(settings.TESTER_INTERVAL).minutes.do(RunTester.start)
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_api():
    # 启动API服务
    ProxyApi.start()

def run():
    """总启动方法"""
    process_list = []
    process_list.append(Process(target=run_spider, name='run_spider'))
    process_list.append(Process(target=run_tester, name='run_tester'))
    process_list.append(Process(target=run_api, name='run_api'))

    # 启动进程
    for p in process_list:
        # 设置进程为守护进行
        p.daemon = True
        # 进程启动
        p.start()

    # 让主进程等待子进程完成
    for p in process_list:
        p.join()

if __name__ == '__main__':
    run()