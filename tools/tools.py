# -*- coding:utf-8 -*-
# @FileName  :tools.py
# @Time      :2020/9/14 15:37
# @Author    :zhm

"""
项目工具代码封装
"""
import random

from common.handle_db import db


def random_name():
    """随机生成一个用户名"""
    while True:
        s1 = random.choice(["a", "b", "c", "d", "e"])
        number = random.randint(100000, 999999)
        name = s1 + str(number)
        # 判断数据库中是否存在该用户名，
        res = db.find_count("SELECT * FROM test.auth_user WHERE username='{}'".format(name))
        if res == 0:
            return name


def assert_dict_item(dic1, dic2):
    """
    断言dic1中的所有元素都是diac2中的成员，不成立引发断言错误
    :param dic1: 字典
    :param dic2: 字典
    :return:
    """
    for item in dic1.items():
        if item not in dic2.items():
            raise AssertionError("{} items not in {}".format(dic1, dic2))


def random_project_name():
    """随机生成一个项目名"""
    while True:
        s1 = random.choice(["前程贷", "开心贷", "新闻APP", "百度新闻001", "腾讯秋秋"])
        number = random.randint(1, 999999)
        name = s1 + str(number)
        # 判断数据库中是否存在该用户名，
        res = db.find_count("SELECT * FROM test.tb_projects WHERE name='{}'".format(name))
        if res == 0:
            return name
