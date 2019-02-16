import logging

# 日志默认的配置
LOG_LEVEL = logging.INFO    # 默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'    # 默认日志文件名称

# 配置开启的爬虫, 默认爬的就是国内的免费代理
PROXIES_SPIDERS = [
    "spiders.proxy_spiders.Daili66ProxySpider",
    "spiders.proxy_spiders.Ip3366ProxySpider",
    "spiders.proxy_spiders.IPhaiProxySpider",
    "spiders.proxy_spiders.ProxylistplusSpider",
    "spiders.proxy_spiders.XiciProxiesSpider"
]

# 检查代理IP超时时间(单位是秒), 如果10s没有返回数据, 就认为该IP不可用
TIMEOUT = 10

# 抓取IP的时间间隔, 单位小时
SPIDER_INTERVAL = 2

# 检查可用IP的时间间隔, 单位分钟
TESTER_INTERVAL = 60

# 检查代理IP的异步数量
TESTER_ANSYC_COUNT = 20

#默认给抓取的ip分配20分,每次连接失败,减一分,直到分数全部扣完从数据库中删除
DEFAULT_SCORE = 20

# 提供可用代理IP的默认数量, 数量越少可用性越高.
DEFAULT_AVAILABLE_IP_COUNT = 20

MONGO_URL = 'mongodb://localhost:27017/'
