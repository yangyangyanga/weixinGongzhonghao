# -*- coding:utf-8 -*-
"""
# @PROJECT: weixinGongzhonghao
# @Author: admin
# @Date:   2018-08-31 10:42:55
# @Last Modified by:   admin
# @Last Modified time: 2018-08-31 10:42:55
"""
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import time


class WeChatSogouSpider(CrawlSpider):
    name = 'wechat'
    allowed_domains = ['weixin.sogou.com', 'mp.weixin.qq.com']
    start_urls = ['http://weixin.sogou.com/weixin?query=python&_sug_type_=&s_from=input&_sug_=n&type=1&page=1&ie=utf8']

    rules = [
        Rule(LinkExtractor(allow=r'page=\d+'), follow=True, callback='page_url'),
    ]
    
    def page_url(self, response):
        print("===============================")
        print(response.url)
        # time.sleep(3)

        # 公众号头像
        icon = response.xpath("//li//div[@class='img-box']//img/@src").extract()
        print(icon)

        # 公众号名
        gongzhonghao_name = response.xpath("//li//div[@class='txt-box']//a[@target='_blank']//text()").extract()
        print(gongzhonghao_name)

        # 微信号
        weichat_num = response.xpath("//li//p[@class='info']/label//text()").extract()
        print(weichat_num)

        # 功能介绍
        function_intro = response.xpath("//li//dl[1]/dd").extract()
        print(function_intro)
        print(len(function_intro))

        # 最近文章
        passage_recently = response.xpath("//li//dl[last()]/dd").extract()
        print(passage_recently)
        print(len(passage_recently))
