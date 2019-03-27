# -*- coding: utf-8 -*-
# @Time    : 2019/2/18 10:08
# @Author  : jiangcheng
# @Email   : jiangcheng@ict.ac.cn
# @File    : baidubaike.py
# @Software: PyCharm
# /**
# 功能:    
# 特殊函数: 
#
# */


import scrapy
import time
from urllib.parse import quote, urljoin
from scrapy_redis.spiders import RedisSpider
import pymysql
import random
from ..items import TripleItem
import re
from ..user_agent import user_agent_list


class Cnkiclass(RedisSpider):
    name = "baidu"
    base_url = "https://baike.baidu.com/"

    def start_requests(self):
        url = "https://baike.baidu.com/item/%E5%8D%97%E6%B5%B7/27429"
        yield scrapy.Request(url, callback=self.parse1, meta={"source_url": url, "times": 0})

    def parse1(self, response):
        source_url = response.meta['source_url']
        times = response.meta['times'] + 1
        entity_name = ''.join(response.xpath('//h1//text()').extract()) + ''.join(
            response.xpath('//h1/../h2//text()').extract())

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "source_url"
        item['prop_val'] = source_url
        yield item

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "full_text"
        item['prop_val'] = response.body
        yield item

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "times"
        item['prop_val'] = times
        yield item

        inforboxs = response.xpath('//div[@class="basic-info cmn-clearfix"]')
        dts = inforboxs.xpath('./dl/dt[@class="basicInfo-item name"]')
        for dt in dts:
            dd = dt.xpath('./following-sibling::dd[1]//text()').extract()
            prop = ''.join(dt.xpath('.//text()').extract()).replace('\n', '').replace('\xa0', '')
            val = ''.join(dd).replace('\n', '').replace('\xa0', '')
            item = TripleItem()
            item['entity_name'] = entity_name
            item['prop_name'] = prop.strip()
            item['prop_val'] = re.sub('\[.*?\]', "", val)
            yield item
            # 打印属性,val
            # print(prop, val)
            # print('-------------------')
        # ##################################################################
        divs = response.xpath('//div[@class="para-title level-2" or @class="para"]')

        text_key = "简介"
        text_val = ""
        for div in divs:
            if div.xpath('./@class').extract_first() == "para":
                text_val += ''.join(div.xpath('.//text()').extract()).replace('\n', '') + " "
            else:
                temp_text_key = ''.join(div.xpath('./h2/text()').extract())
                if text_val != temp_text_key:
                    item = TripleItem()
                    item['entity_name'] = entity_name
                    item['prop_name'] = text_key
                    item['prop_val'] = re.sub('\[.*?\]', "", text_val.replace('\xa0', ''))
                    yield item
                    # key and val
                    # print(text_key)
                    # print(text_val)
                    # print('-----')
                    text_val = ""
                text_key = temp_text_key
        else:
            item = TripleItem()
            item['entity_name'] = entity_name
            item['prop_name'] = text_key
            item['prop_val'] = re.sub('\[.*?\]', "", text_val.replace('\xa0', ''))
            yield item

        # next url
        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "response_url"
        item['prop_val'] = response.url
        yield item

        all_links = response.xpath('//a[contains(@target,"_blank")]/@href').extract()
        for link in all_links:
            if re.findall(r'/item/.*', link):
                nexturl_pre = urljoin(self.base_url, link)
                try:
                    nexturl = nexturl_pre.split("?")[0]
                except:
                    print(nexturl_pre)
                    nexturl = nexturl_pre
                yield scrapy.Request(nexturl, callback=self.parse1,
                                     meta={"source_url": response.url, "times": times})
