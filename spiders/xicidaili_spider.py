import time
import random

from spiders.spider import ProxySpider
"""
西刺代理
"""
class XiciProxiesSpider(ProxySpider):
    urls = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 2)]
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    detail_xpath = {'ip': './td[2]', 'port':'./td[3]', 'area':'./td[4]'}

    def get_page_from_url(self, url):
        # 由于西刺对访问频率有限制,我们随机1,5秒, 请求一次
        time.sleep(random.uniform(1, 5))
        return super().get_page_from_url(url)

if __name__ == '__main__':
    spider = XiciProxiesSpider()
    for proxy in spider.get_proxies():
        print(proxy)

