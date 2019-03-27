# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from .user_agent import user_agent_list
from scrapy import signals
# 导入动态ua
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
# 导入代理ip
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import requests


class MyspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class QianlongwangSpiderMiddleware(object):
    """
        从网上找到的其他人的中间键
    """
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_error, signal=signals.spider_error)
        crawler.signals.connect(s.spider_idle, signal=signals.spider_idle)

        return s

    # 当spider开始爬取时发送该信号。该信号一般用来分配spider的资源，不过其也能做任何事。
    def spider_opened(self, spider):
        spider.logger.info('爬虫启动: %s' % spider.name)
        print('start', '1')

    def item_scraped(self, item, response, spider):
        pass

    # 当某个spider被关闭时，该信号被发送。该信号可以用来释放每个spider在 spider_opened 时占用的资源。
    def spider_closed(self, spider, reason):
        print('-------------------------------all over------------------------------------------')
        # print(spider.par)
        # print(spider.name, ' closed')

    # 当spider的回调函数产生错误时(例如，抛出异常)，该信号被发送。
    def spider_error(self, failure, response, spider):
        code = response.status
        print('spider error + %s' % code)

    # 当spider进入空闲(idle)状态时该信号被发送。空闲意味着:
    #    requests正在等待被下载
    #    requests被调度
    #    items正在item pipeline中被处理
    def spider_idle(self, spider):
        for i in range(3):
            print(spider.name)


class UAPools(UserAgentMiddleware):
    """
        更换user_agent
    """
    def __init__(self, user_agent=''):
        self.user_agent = user_agent
        self.user_agent_list = user_agent_list

    def process_request(self, request, spider):
        try:
            ua = random.choice(self.user_agent_list)
            if ua:
                request.headers.setdefault('User-Agent', ua)

        except Exception as e:
            print(e)
            pass


# class IpPools(HttpProxyMiddleware):
#     def __init__(self, ip=''):
#
#         self.ippools = ips
#         self.ip = ip
#
#     def process_request(self, request, spider):
#         try:
#             ip = random.choice(self.ippools)
#             request.meta['proxy'] = "http://" + ip
#             # request.meta['proxy'] = "https://" + self.ip
#         except Exception as e:
#             print(e)
#             pass


import base64
# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"
# 代理隧道验证信息
proxyUser = "H5GB7Q88131C73BD"
proxyPass = "DE597CD9015011DB"
# for Python2
# proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth
