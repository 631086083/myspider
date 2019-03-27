# -*- coding: utf-8 -*-
# @Time    : 2019/2/18 10:42
# @Author  : jiangcheng
# @Email   : jiangcheng@ict.ac.cn
# @File    : hudong.py
# @Software: PyCharm
# /**
# 功能:    
# 特殊函数: 
#
# */
import scrapy

import scrapy
import time
from urllib.parse import quote

import pymysql
import random
from items import TripleItem
import re
from ..user_agent import user_agent_list
from scrapy_redis.spiders import RedisSpider
import json


class Cnkiclass(RedisSpider):
    name = "hudong"

    def start_requests(self):
        # keywords = ["国家", "各国历史", "历史事件", "社会问题", "社会事件", "灾难", "贸易", "企业", "金融", "经济组织", "机构", "社会组织", "行业组织", "政府组织",
        #             "政治人物", "自然科学人物", "社会科学人物", "财经人物", "经济人物", "历史名人", "军事人物", "军队", "军事兵种", "战争", "战役", "行政区划",
        #             "行政区域", "地理名称", "地理位置", "海峡", "军区", "港口", "车站", "机场", "军事装备", "飞机", "战术导弹", "战略导弹", "科技", "设备"]
        # for keyword in keywords:
        #     url = "http://fenlei.baike.com/category/Ajax_cate.jsp?catename=" + quote(keyword)
        #     yield scrapy.Request(url, callback=self.all_kinds)
        keyword_lists = [
            ["国家", "各国历史"],
            ["历史事件", "社会问题", "社会事件", "灾难", "贸易"],
            ["企业", "金融", "经济组织", "机构", "社会组织", "行业组织", "政府组织"],
            ["政治人物", "自然科学人物", "社会科学人物", "财经人物", "经济人物", "历史名人", "军事人物"],
            ["军队", "军事兵种"],
            ["战争", "战役"],
            ["行政区划", "行政区域", "地理名称", "地理位置", "海峡", "军区"],
            ["港口", "车站", "机场"],
            ["军事装备", "飞机", "战术导弹", "战略导弹", "科技", "设备"]
        ]
        for index, keywords in enumerate(keyword_lists):
            for keyword in keywords:
                url = "http://fenlei.baike.com/category/Ajax_cate.jsp?catename=" + quote(keyword)
                yield scrapy.Request(url, callback=self.all_kinds, meta={"species": keyword, "index": index})

    def all_kinds(self, response):
        species = response.meta['species']
        index = response.meta['index']
        kinds = json.loads(response.text)
        if kinds:
            for kind in kinds:
                keyword = kind['name']
                nexturl = "http://fenlei.baike.com/" + keyword + "/list/"
                kind_url = "http://fenlei.baike.com/category/Ajax_cate.jsp?catename=" + quote(keyword)
                yield scrapy.Request(kind_url, callback=self.all_kinds, meta={"species": species, "index": index})
                yield scrapy.Request(nexturl, callback=self.final_kind,
                                     meta={"kind": keyword, "species": species, "index": index})

    def final_kind(self, response):
        species = response.meta['species']
        index = response.meta['index']
        keyword = response.meta['kind']
        next_urls = response.xpath('//dd/a/@href').extract()
        for next_url in next_urls:
            if next_url.startswith("http"):
                yield scrapy.Request(next_url, callback=self.parse_leaf,
                                     meta={"kind": keyword, "species": species, "index": index})

    def parse_leaf(self, response):
        kind = response.meta['kind']
        species = response.meta['species']
        index = response.meta['index']
        entity_name = ''.join(response.xpath('//h1/text()').extract())

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "####kind####"
        item['prop_val'] = kind
        yield item

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "####species####"
        item['prop_val'] = species
        yield item

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "####index####"
        item['prop_val'] = str(index)
        yield item

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "full_text"
        item['prop_val'] = response.body
        yield item

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "response_url"
        item['prop_val'] = response.url
        yield item

        openCatp = response.xpath('//p[@id="openCatp"]//text').extract()
        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = "openCaptl"
        item['prop_val'] = ' '.join(openCatp)
        yield item

        inforboxs = response.xpath('//div[@class="module zoom"]/table')
        for inforbox in inforboxs:
            trs = inforbox.xpath('.//tr')
            for tr in trs:
                # for cgl in range(1, len(tr.xpath('./td').extract())):
                for cgl in (1, 3):
                    prop = tr.xpath('./td[' + str(cgl) + ']/strong//text()').extract()
                    val = tr.xpath('./td[' + str(cgl) + ']/span//text()').extract()
                    prop = ''.join(prop)
                    val = ''.join(val)
                    # print(prop, val)
                    # print('------')
                    item = TripleItem()
                    item['entity_name'] = entity_name
                    item['prop_name'] = prop
                    item['prop_val'] = re.sub('\[.*?\]', "", val.replace('\xa0', '').replace('\t', ''))
                    yield item
        # ##################################################################################
        txt_key = "baseline"
        txt_val = ''.join(response.xpath('//div[@class="summary"]/p//text()').extract())

        item = TripleItem()
        item['entity_name'] = entity_name
        item['prop_name'] = txt_key
        item['prop_val'] = re.sub('\[.*?\]', "", txt_val.replace('\xa0', '').replace('\t', ''))
        yield item

        txt_key = ""
        txt_val = ""
        txts = response.xpath('//div[@id="content"]/text()|//div[@id="content"]/*')
        for txt in txts:
            if txt.xpath('./self::div[contains(@class,"content_h2")]'):
                temp_key = ''.join(txt.xpath('./self::*[contains(@class,"content_h2")]/h2/text()').extract()).replace(
                    '\n', '')
                if temp_key != txt_key:
                    if txt_key:
                        # print('------')
                        # print(txt_key)
                        # print(txt_val)
                        # print('------')
                        item = TripleItem()
                        item['entity_name'] = entity_name
                        item['prop_name'] = txt_key.strip()
                        item['prop_val'] = re.sub('\[.*?\]', "", txt_val.replace('\xa0', '').replace('\t', ''))
                        yield item
                        txt_val = ""
                    else:
                        pass
                    txt_key = temp_key

            elif txt.xpath('./self::p'):
                txt_val += ''.join(txt.xpath('.//text()').extract()).replace('\n', '') + ' '

            elif txt.xpath('./self::div'):
                txt_val += ''.join(
                    txt.xpath('./descendant-or-self::*[not(contains(@class,"img"))]//text()').extract()).replace('\n',
                                                                                                                 '') + ' '
            elif type(txt.root) == str:
                txt_val += txt.root.replace('\n', '') + ' '
            else:
                txt_val += ''.join(txt.xpath('.//text()').extract()).replace('\n', '') + ' '
        else:
            # print('------')
            # print(txt_key)
            # print(txt_val)
            # print('------')
            item = TripleItem()
            item['entity_name'] = entity_name
            item['prop_name'] = txt_key.strip()
            item['prop_val'] = re.sub('\[.*?\]', "", txt_val.replace('\xa0', '').replace('\t', ''))
            yield item
