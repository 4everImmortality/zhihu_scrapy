#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from zhihu.dbtools import *
import datetime


class ZhihuPipeline:
    def process_item(self, item, spider):
        content_str = ', '.join(map(lambda x: str(x), item['content'])) if item['content'] else None
        sql = 'insert into `ZH_wt`(`username`,`dateModified`,`content`,`personalInfo`) values(%s,%s,%s,%s)'
        params = (item['username'][0], item['dateModified'][0], content_str, item['personalInfo'])
        affectedRows = dbExecute(sql, params)

        if affectedRows > 0:
            print('数据库添加成功')
        else:
            print('数据库添加失败')
        return item
