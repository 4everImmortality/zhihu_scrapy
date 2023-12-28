# python3
# -*- coding: utf-8 -*-
# @Time    : 2023/12/27 9:15
# @Author  : 10148

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import re

# 读取mysql数据库 读取数据库使用with语句
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/db_scrapy?charset=utf8mb4')
sql = 'select * from zh_wt'
df = pd.read_sql(sql, engine)
# 显示前10个
df.set_index('mid', inplace=True)
# print(df.head(10))
# print(df.info())
# 对PersonalInfo字段进行分词
print(df['personalInfo'].head())
# 1. 去除',' '。'等各类中英文标点符号
df['personalInfo'] = df['personalInfo'].str.replace(r'[^\w\s]+', '', regex=True)
print(df['personalInfo'].head())

# 分词
words = jieba.lcut(df['personalInfo'].str.cat(sep=' '))
print(words[:10])
# 去除停用词
stopwords = []
with open('baidu_stopwords.txt', encoding='utf-8') as f:
    for line in f.readlines():
        stopwords.append(line.strip())

stopwords.append('个人说明')
print(stopwords[:10])
# 去除单个字
words = [word for word in words if len(word) > 1]
# 去除停用词
words = [word for word in words if word not in stopwords]
# 词频统计
word_count = pd.Series(words).value_counts()
print(word_count.head(10))
# 词云
font = r'C:\Windows\Fonts\simfang.ttf'
wc = WordCloud(font_path=font, background_color='white', width=1600, height=1200, max_words=200)
wc.generate_from_frequencies(word_count)
plt.imshow(wc)
plt.axis('off')
plt.tight_layout()
plt.show()

# 词云保存
wc.to_file('wordcloud_PersonalInfo.png')
