# -*- coding: utf-8 -*-

# Scrapy settings for myspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'myspider'

SPIDER_MODULES = ['myspider.spiders']
NEWSPIDER_MODULE = 'myspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'myspider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 下载延时
# DOWNLOAD_DELAY = 3

# 并发数修改
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# 发送cookie设置
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# 爬虫中间件使能控制
# SPIDER_MIDDLEWARES = {
#    'myspider.middlewares.MyspiderSpiderMiddleware': 543,
#   #'myspider.middlewares.QianlongwangSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# 下载中间件使能控制
DOWNLOADER_MIDDLEWARES = {
    # 'myspider.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 125,
    'myspider.middlewares.UAPools': 126,
    # 'myspider.middlewares.IpPools': 124,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 123,
    # 'myspider.middlewares.MyCustomDownloaderMiddleware': 543,
    # 'scrapy_crawlera.CrawleraMiddleware': 600
    # 'myspider.middlewares.ProxyMiddleware': 127,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# 扩展配置使能控制
# MYEXT_ENABLED = True  # 开启扩展
# IDLE_NUMBER = 50  # 配置空闲持续时间单位为 360个 ，一个时间单位为5s
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#    'myspider.extensions.RedisSpiderSmartIdleClosedExensions': 500,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# 入库函数使能控制
ITEM_PIPELINES = {
    # 'myspider.pipelines.MyspiderPipeline': 300,
    'myspider.pipelines.MysqlTwistedPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# # -------------------
# # 队列优先级配置
# # -------------------
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

# # -------------------
# # mysql库配置
# # -------------------
MYSQL_HOST = '10.60.1.103'
MYSQL_DBNAME = 'jkw_baike'
MYSQL_USER = 'jiangcheng'
MYSQL_PASSWORD = '07fa533360d9'

# # -------------------
# # MongoDB库配置
# # -------------------
# MONGODB 主机名
MONGODB_HOST = "127.0.0.1"
# MONGODB 端口号
MONGODB_PORT = 27017
# 数据库名称
MONGODB_DBNAME = "admin"
# 存放数据的表名称
MONGODB_SHEETNAME = "uss"

# # -------------------
# # 加速配置
# # -------------------
LOG_LEVEL = 'INFO'
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 15

# # #####################
# # #scrapy_redis扩展配置
# # #####################
#
# # # -------------------
# # #redis配置
# # # -------------------
# REDIS_URL = 'redis://10.61.2.167:6379/8'
#
# # # -------------------
# # # scrapy_redis 配置
# # # -------------------
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = False
#
# # # -------------------
# # # 队列优先级配置
# # # -------------------
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy_redis.squeues.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy_redis.squeues.FifoMemoryQueue'
