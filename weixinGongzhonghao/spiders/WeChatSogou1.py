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
import time, datetime
from selenium import webdriver
import re
from weixinGongzhonghao.items import WeixingongzhonghaoItem

class WeChatSogou1Spider(scrapy.Spider):
    name = 'wechat1'
    allowed_domains = ['weixin.sogou.com', 'mp.weixin.qq.com']
    start_urls = ['https://weixin.sogou.com/']

    def parse(self, response):
        print("===============================")
        print(response.url)
        # time.sleep(3)

        driver = webdriver.Chrome(r"C:\Users\admin\AppData\Local\Programs\Python\Python36\Lib\site-packages\selenium\chromedriver (2).exe")
        # driver.implicitly_wait(30)
        driver.get(response.url)
        # 美国学术作假、美国OPT、美国H1B签证、美国买车、美国酒驾、美国超速、美国交通事故、美国罚单、美国种族歧视、美国校园纠纷
        '''
        美国留学从第8页断开
        '''
        search_keywords = ["美国留学", "美国保险", "美国安全", "美国学术作假", "美国OPT", "美国H1B签证", "美国实习",
                           "美国就业", "美国创业", "美国租房", "美国买车", "美国酒驾", "美国超速", "美国法律", "美国律师",
                           "美国交通事故", "美国罚单", "美国种族歧视", "美国校园纠纷", "美国性骚扰", "Airbnb"]
        # for search_keyword in search_keywords:
        search_keyword = "美国留学"
        print("search_keyword: ", search_keyword)
        driver.find_element_by_xpath('//*[@id="query"]').send_keys(search_keyword)
        driver.find_element_by_xpath('//*[@id="searchForm"]/div/input[4]').click()
        time.sleep(16)
        detail_url = driver.current_url
        print("====", detail_url)
        print(driver, "1")
        # driver.switch_to_window()
        yield scrapy.Request(detail_url, callback=self.parse_data, meta={"driver": driver, "search_keyword": search_keyword})
        # driver.close()

    def parse_data(self, response):
        time.sleep(3)
        driver = response.meta['driver']
        print(driver, "2")
        item = self.get_item()
        item["create_time"] = datetime.datetime.now()
        item["search_keyword"] = response.meta['search_keyword']
        item["source_location"] = "微信"
        item["company_url"] = response.url

        try:
            for i in range(10):
                print("===============================", str(i))
                key_id = "sogou_vr_11002301_box_" + str(i)
                # 公众号名
                gongzhonghao_name = driver.find_element_by_xpath(
                    "//li[@id='" + key_id + "']//div[@class='txt-box']//a[@target='_blank']").text
                print("gongzhonghao_name: ", gongzhonghao_name)
                item["title"] = gongzhonghao_name

                # 微信号
                weichat_num = driver.find_element_by_xpath("//li[@id='" + key_id + "']//p[@class='info']/label").text
                print("weichat_num: ", weichat_num)
                item["weichat_name"] = weichat_num


                # 功能介绍
                try:
                    function_intro = driver.find_element_by_xpath(
                        "//li[@id='" + key_id + "']//dt[contains(text(),'功能介绍：')]/../dd").text
                except Exception as e:
                    function_intro = None
                print("function_intro: ", function_intro)
                # print(len(function_intro))
                item["function_intro"] = function_intro

                # 最近文章
                try:
                    passage_recently = driver.find_element_by_xpath(
                        "//li[@id='" + key_id + "']//dt[contains(text(),'最近文章：')]/../dd").text
                    posting_time = driver.find_element_by_xpath(
                        "//li[@id='" + key_id + "']//dt[contains(text(),'最近文章：')]/../dd/span").text
                except Exception as e:
                    passage_recently = None
                    posting_time = None
                print("passage_recently: ", passage_recently)
                item["passage_recently"] = passage_recently
                item['posting_time'] = posting_time
                print("posting_time: ", posting_time)

                # 微信认证
                try:
                    wechat_auth = driver.find_element_by_xpath("//li[@id='" + key_id + "']//dl[2]/dd").text
                except Exception as e:
                    wechat_auth = None
                print("wechat_auth: ", wechat_auth)
                item["company_name"] = wechat_auth


                # 月发文
                month_passage_yuan = driver.find_element_by_xpath("//li[@id='" + key_id + "']//p[@class='info']").text
                month_passage_re = re.findall(r"月发文(.*)篇", month_passage_yuan)
                month_passage = ''.join(month_passage_re).strip()
                print("month_passage: ", month_passage)
                # print(len(passage_recently))
                item["month_passage"] = month_passage

                # 来源链接，公众号链接
                current_handle = driver.current_window_handle
                print("current_handle: ", current_handle)
                driver.find_element_by_xpath("//li[@id='" + key_id + "']//div[@class='txt-box']//a[@target='_blank']").click()
                time.sleep(15)
                all_handels = driver.window_handles
                print("all_handels: ", all_handels)
                driver.switch_to_window(all_handels[-1])

                current_handle = driver.current_window_handle
                print("current_handle1: ", current_handle)

                company_url = driver.current_url
                print("company_url: ", company_url)
                time.sleep(3)
                driver.close()      # 关闭新打开的标签页
                driver.switch_to_window(all_handels[0])     # 跳转到列表标签页
                time.sleep(10)
                item["url"] = company_url
                yield item

        except Exception as e:
            print("id异常===", str(e))
            with open("weichat_error.txt", "a+") as f:
                f.write("id异常===" + str(e) + "\n")
        # 下一页
        try:
            next = driver.find_element_by_id("sogou_next").get_attribute('href')
            print("next: ", next)
            driver.get(next)
            # try:
                # next_1 = driver.find_element_by_id("sogou_next").get_attribute('href')
                # if next_1:
            yield scrapy.Request(next, callback=self.parse_data, meta={"driver": driver, "search_keyword": item['search_keyword']})
            # except Exception as e:
            #     print("最后一页====", str(e))

        except Exception as e:
            print("没有下一页====", str(e))
            with open("weichat_keyword_end_url.txt", "a+", encoding='utf-8') as f:
                f.write("关键字搜索最后一页链接===" + response.url + "\n")

    def get_item(self):
        item = WeixingongzhonghaoItem()
        item["title"] = None
        item["company_name"] = None
        item["weichat_name"] = None
        item["company_url"] = None
        item["function_intro"] = None
        item["passage_recently"] = None
        item["month_passage"] = None
        item["answer_num"] = None
        item["read_num"] = None
        item["good_num"] = None
        item["posting_time"] = None
        item["create_time"] = None
        item["search_keyword"] = None
        item["url"] = None
        item["source_location"] = None
        return item