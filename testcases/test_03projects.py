# -*- coding:utf-8 -*-
# @FileName  :test_03projects.py
# @Time      :2020/9/14 17:33
# @Author    :zhm
"""
测试创建项目接口用例
"""

import os
import unittest
import requests
from common import myddt
from common.handle_db import db
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_log import log
from jsonpath import jsonpath
from common.handle_data import replace_data
from tools.tools import random_project_name, assert_dict_item


@myddt.ddt
class TestProjects(unittest.TestCase):
    excel = HandleExcel(file_name=os.path.join(DATA_DIR, 'apicases.xlsx'), sheet_name='projects')
    cases_data = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        """请求登录，获取token"""
        login_url = conf.get('env', 'base_url') + '/user/login/'
        params = {
            "username": conf.get('test_data', 'username'),
            "password": conf.get('test_data', 'password')
        }
        response = requests.request(method='post', url=login_url, json=params)
        res = response.json()
        token_value = jsonpath(res, '$.token')[0]
        cls.token = 'JWT' + ' ' + token_value

        # 查询数据库中已存在的项目名称
        name = db.find_one('SELECT NAME FROM test.tb_projects LIMIT 1')
        cls.be_project_name = name['NAME']

    def setUp(self):
        TestProjects.project_name = random_project_name()

    @myddt.data(*cases_data)
    def test_projects(self, case):
        # 请求接口
        url = conf.get('env', 'base_url') + case['url']
        # 请求参数
        params = eval(replace_data(case['data'], TestProjects))
        # 请求方法
        method = case['method']
        # 请求头
        headers = {"Authorization": self.token}
        # 预期结果
        expected = eval(replace_data(case['expected'], TestProjects))
        # 获得实际结果
        response = requests.request(method=method, url=url, json=params, headers=headers)
        res = response.json()

        print('预期结果：', expected)
        print('实际结果：', res)

        # 断言
        try:
            self.assertEqual(response.status_code, case['code'])
            assert_dict_item(expected, res)
        except AssertionError as e:
            log.error('用例{}，执行未通过'.format(case['title']))
            log.exception(e)
            self.excel.write_excel(row=case['case_id'] + 1, column=9, value='未通过')
            raise e
        else:
            log.info('用例{}，执行通过'.format(case['title']))
            self.excel.write_excel(row=case['case_id'] + 1, column=9, value='通过')
