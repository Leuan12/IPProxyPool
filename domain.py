from settings import DEFAULT_SCORE

# 代理模型类, 用于封装代理相关信息
class Proxy(object):
    def __init__(self, ip, port, protocol=-1, nick_type=-1,speed=-1, area=None, score=DEFAULT_SCORE):
        self.ip = ip    # IP
        self.port = port # 端口号
        self.protocol = protocol   # 协议: http与https:2, http:0, https:1
        self.nick_type = nick_type #  匿名程度:高匿:0,匿名: 1, 透明:2
        self.speed = speed # 速度, 单位s
        self.area = area   # 地区
        self.score = score # 代理IP的评分

    def __hash__(self):
        return hash(self.ip)

    def __eq__(self, other):
        if isinstance(other, Proxy):
            return self.ip == other.ip
        else:
            return False

    @property
    def dict(self):
        return dict(self.__dict__)

    def __str__(self):
        # 返回数据字符串
        return str(self.__dict__)

if __name__ == '__main__':
    proxy = Proxy('xx', '0')
    # print(proxy.dict)
    proxy_1 = Proxy('xx', '0')

    cache = set()
    print(cache.add(proxy))
    print(cache.add(proxy_1))
    for p in cache:
        print(p)




