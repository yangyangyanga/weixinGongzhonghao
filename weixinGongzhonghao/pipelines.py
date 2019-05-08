# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class WeixingongzhonghaoPipeline(object):
    db = pymysql.connect("rm-2ze60394nj37p9q9n6o.mysql.rds.aliyuncs.com", "shujuzu", "pythonshujuzu", "hooli_law", charset='utf8')
    cursor = db.cursor()

    count = 1  # 控制最大的批次号不变
    batch_number = 1

    def process_item(self, item, spider):
        insert_sql = "insert into us_law(title, company_name, weichat_name, company_url, function_intro, passage_recently, " \
                     "month_passage, answer_num, read_num, good_num, posting_time, create_time, search_keyword, url, source_location) " \
                     "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                     "%s, %s, %s, %s, %s, %s)"
        # print("insert_sql: ", insert_sql)
        try:
            self.cursor.execute(insert_sql, (item["title"], item["company_name"], item["weichat_name"], item["company_url"], 
                                             item["function_intro"], item["passage_recently"], item["month_passage"], item["answer_num"], 
                                             item["read_num"], item["good_num"], item["posting_time"], item["create_time"], item["search_keyword"], 
                                             item["url"], item["source_location"]))
            self.db.commit()
            print("数据插入成功")
        except Exception as e:
            self.db.rollback()
            print("数据插入失败：%s" % (str(e)))
            with open(r"D:\pycharm\Study\weixinGongzhonghao\mysqlerror\mysqlerror_sql.txt", 'a', encoding="utf-8") as f:
                f.write(str(e) + "\n" + item['url'] + "\n========================\n")
        # self.cursor.close()
        # self.db.close()
        return item
