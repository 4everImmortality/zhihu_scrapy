# python3
# -*- coding: utf-8 -*-
# @Time    : 2023/12/22 10:52
# @Author  : 10148

import pymysql
import traceback

'''
    参数名称
    host：连接的数据库服务器主机名，默认为localhost
    port：连接的数据库服务器端口号，默认为3306
    user：连接数据库的用户名，默认为当前用户
    passwd：连接数据库的密码，没有默认值
    db：连接的数据库名，没有默认值
'''
host = 'localhost'
port = 3306
user = 'root'
password = '123456'
db = 'db_scrapy'
charset = 'utf8'


def dbExecute(sql, params=()):
    conn, cursor = None, None
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        cursor = conn.cursor()
        affectedRows = cursor.execute(sql, params)
        conn.commit()
        print('commit success')
        return affectedRows
    except:
        if conn:
            conn.rollback()
        print('commit fail')
        traceback.print_exc()
        return -1
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def dbQueryOne(sql, params=()):
    conn, cursor = None, None
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()
    except:
        traceback.print_exc()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def dbQueryAll(sql, params=()):
    conn, cursor = None, None
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    except:
        traceback.print_exc()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
