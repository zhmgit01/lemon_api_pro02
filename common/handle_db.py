# -*- coding:utf-8 -*-
# @FileName  :handle_db.py
# @Time      :2020/9/14 14:06
# @Author    :zhm

"""
封装数据库操作类
"""

import pymysql
from common.handle_config import conf


class HandleDB:

    def __init__(self, host, user, password, port, charset):
        """初始化方法"""
        # 1、创建数据库连接
        self.con = pymysql.connect(host=host,
                                   user=user,
                                   password=password,
                                   port=port,
                                   charset=charset,
                                   cursorclass=pymysql.cursors.DictCursor)
        # 2、创建游标
        self.cur = self.con.cursor()

    def find_data(self, sql):
        """查询数据方法"""
        # 提交事务，同步数据库的状态
        self.con.commit()
        # 使用execute()方法执行sql方法
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res

    def find_count(self, sql):
        """返回查询数据的条数"""
        self.con.commit()
        return self.cur.execute(sql)

    def find_one(self, sql):
        """获取查询出来的第一条数据"""
        # 执行查询语句
        self.con.commit()
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data


db = HandleDB(host=conf.get('database', 'host'),
              user=conf.get('database', 'user'),
              password=conf.get('database', 'password'),
              port=conf.getint('database', 'port'),
              charset=conf.get('database', 'charset'), )
