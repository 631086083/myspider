# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# class D4Item(scrapy.Item):
#     acm_citations = scrapy.Field()
#     name_en = scrapy.Field()
#     name_zh = scrapy.Field()
#     aminerid = scrapy.Field()
#     desc = scrapy.Field()
#     ethnic = scrapy.Field()
#     gender = scrapy.Field()
#     lang = scrapy.Field()
#     nation = scrapy.Field()
#     address = scrapy.Field()
#     affiliation = scrapy.Field()
#     activity = scrapy.Field()
#     diversity = scrapy.Field()
#     g_index = scrapy.Field()
#     h_index = scrapy.Field()
#     num_citation = scrapy.Field()
#     num_pubs = scrapy.Field()
#     sociability = scrapy.Field()
#     url = scrapy.Field()
#     pos = scrapy.Field()
#     tags = scrapy.Field()
#     avatar = scrapy.Field()
#     t_index = scrapy.Field()


class UssItem(scrapy.Item):
    wname = scrapy.Field()
    wsubtype = scrapy.Field()
    wprop = scrapy.Field()
    wval = scrapy.Field()


class TripleItem(scrapy.Item):
    entity_name = scrapy.Field()
    prop_name = scrapy.Field()
    prop_val = scrapy.Field()
    type = scrapy.Field()
