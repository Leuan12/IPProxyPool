import pymongo
import random

from settings import MONGO_URL, DEFAULT_SCORE, DEFAULT_AVAILABLE_IP_COUNT
from domain import Proxy

class MongoPool(object):
    def __init__(self):
        """初始化"""
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client.proxy
        self.proxys = self.db.proxys

    def drop_db(self):
        """删除数据库"""
        self.client.drop_database(self.db)

    def insert(self, proxy=None):
        """插入代理IP"""
        if proxy:
            dic = proxy.dict
            dic['_id'] =  proxy.ip
            self.proxys.save(dic)

    def delete(self, proxy=None):
        """根据条件删除代理IP"""
        if proxy:
            self.proxys.remove({'_id':proxy.ip})
            return ('deleteNum', 'ok')
        else:
            return ('deleteNum', 'None')


    def update(self, proxy=None):
        """更新代理"""
        if proxy:
            self.proxys.update({'_id':proxy.ip}, {"$set": proxy.dict})
            return {'updateNum': 'ok'}
        else:
            return {'updateNum': 'fail'}

    def select(self, count=None, conditions=None):
        if count:
            count = int(count)
        else:
            count = 0

        if conditions:
            conditions = dict(conditions)
            if 'count' in conditions:
                del conditions['count']
        else:
            conditions = {}

        items = self.proxys.find(conditions, limit=count).sort(
            [("speed", pymongo.ASCENDING), ("score", pymongo.DESCENDING)])
        results = []
        for item in items:
            result = Proxy(item['ip'], item['port'],
                           score=item['score'], protocol=item['protocol'],
                           nick_type=item['nick_type'], speed=item['speed'])
            results.append(result)
        return results

    def find_proxy_by_ip(self, ip):
        item = self.proxys.find_one({'_id': ip})
        if item:
            return Proxy(item['ip'], item['port'],
                  score=item['score'], protocol=item['protocol'],
                  nick_type=item['nick_type'], speed=item['speed'])
        else:
            return None

    def get_proxeis(self, protocol='http',  count=DEFAULT_AVAILABLE_IP_COUNT):
        conditions = {'protocol': protocol.lower()}
        return self.select(count, conditions)

    def all(self, protocol=None,  count=DEFAULT_AVAILABLE_IP_COUNT):
        """
        获取所有代理IP
        :param protocol: 协议: http or https
        :return: 如果传入协议, 就只获取高匿的, 分数为最高的
        """
        print(count)
        if protocol is None:
            return self.select()
        elif protocol.lower() == 'http':
            return self.select(count=count, conditions={"protocol": {'$in': [2, 0]}, 'nick_type':0, 'score':DEFAULT_SCORE})
        elif protocol.lower() == 'https':
            return self.select(count=count, conditions={"protocol": {'$in': [2, 1]}, 'nick_type':0, 'score':DEFAULT_SCORE})
        return []

    def random(self, protocol=None, count=DEFAULT_AVAILABLE_IP_COUNT):
        """随机获取一个一个代理IP"""
        proxy_list = self.all(protocol, count=count)
        return random.choice(proxy_list)

    def resume_score(self, proxy):
        """恢复代理分数"""
        # 更新分数
        self.proxys.update({'_id': proxy.ip}, {"$set": {"score": DEFAULT_SCORE}})

    def decrease_score(self, proxy):
        # 如果没有分数, 就从数据库获取该IP信息, 再进行更新
        if proxy.score == -1:
            proxy = self.find_proxy_by_ip(proxy.ip)

        # 让代理分数减少1
        proxy.score -= 1
        # 更新分数
        self.proxys.update({'_id':proxy.ip}, {"$set": {"score":proxy.score}})


if __name__ == '__main__':
    import requests
    from utils.request import get_header
    pool = MongoPool()
    # for a in pool.all('http'):
    url = 'http://www.baidu.com'
    a = pool.random('http')
    proxies = {'http': '{}:{}'.format(a.ip, a.port)}
    print(proxies)
    response = requests.get(url, headers=get_header(), proxies=proxies)
    print(response.status_code)
    print(response.content.decode())




