# python3
# -*- coding: utf-8 -*-
# @Time    : 2023/12/26 11:12
# @Author  : 10148

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import re

# 读取mysql数据库
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/db_scrapy?charset=utf8mb4')
# 统计匿名用户的数量
sql = 'select count(*) from zh_wt where username="匿名用户"'
# 统计非匿名用户的数量
sql2 = 'select count(*) from zh_wt where username!="匿名用户"'
df = pd.read_sql(sql, engine)
df2 = pd.read_sql(sql2, engine)
print(df)
print(df2)
# 画饼图，显示匿名用户和非匿名用户的比例在一张图上
# 0. 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
# 设置字体大小
plt.rcParams['font.size'] = 12
# 1. 准备数据
# 1.1 准备标签
labels = ['匿名用户', '非匿名用户']
# 1.2 准备数据
sizes = [df['count(*)'][0], df2['count(*)'][0]]
# 1.3 准备颜色 渐变色
colors = ['red', 'dodgerblue']
# 修改背景颜色
plt.rcParams['axes.facecolor'] = 'gold'

# 1.4 准备突出显示
explode = [0.05, 0]
# 2. 画饼图
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=150)
# 设置标题
plt.title('用户匿名与非匿名比例', fontsize=16, fontweight='bold', color='navy')  # 设置标题
plt.axis('equal')  # 使饼图更圆
# 调整图例位置
plt.legend(loc='upper right')
#  添加注释
plt.annotate(f"{sizes[0]} 个", xy=(-0.8, 0.3), xytext=(-1.0, 0.8), fontsize=12, color='red',
             arrowprops=dict(facecolor='red', arrowstyle='->'))
# 4. 显示图形
plt.tight_layout()
# 保存饼图
plt.savefig('pie.png')

plt.show()
