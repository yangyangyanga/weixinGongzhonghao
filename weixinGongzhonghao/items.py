# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixingongzhonghaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    company_name = scrapy.Field()
    weichat_name = scrapy.Field()
    company_url = scrapy.Field()
    function_intro = scrapy.Field()
    passage_recently = scrapy.Field()
    month_passage = scrapy.Field()
    answer_num = scrapy.Field()
    read_num = scrapy.Field()
    good_num = scrapy.Field()
    posting_time = scrapy.Field()
    create_time = scrapy.Field()
    search_keyword = scrapy.Field()
    url = scrapy.Field()
    source_location = scrapy.Field()



