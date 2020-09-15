# -*- coding:utf-8 -*-
# @FileName  :test_04interface.py
# @Time      :2020/9/14 18:10
# @Author    :zhm
"""
测试新增接口 的接口的用例类
"""

import os
import requests
import unittest
from jsonpath import jsonpath
from common.handle_config import conf
from common.handle_excel import HandleExcel
from common.handle_log import log
from common.handle_path import DATA_DIR
from common import myddt
from common.handle_data import replace_data
from tools.tools import random_project_name, assert_dict_item


@myddt.ddt
class TestInterface(unittest.TestCase):
    excel = HandleExcel(file_name=os.path.join(DATA_DIR, 'apicases.xlsx'), sheet_name='interface')
    cases_data = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        """新增接口用例执行前数据准备"""

        # 请求登录接口获取token
        login_url = conf.get('env', 'base_url') + '/user/login/'
        login_params = {
            "username": conf.get('test_data', 'username'),
            "password": conf.get('test_data', 'password')
        }
        response = requests.request(method='post', url=login_url, json=login_params)
        res = response.json()
        token_value = jsonpath(res, '$.token')[0]
        cls.token = 'JWT' + ' ' + token_value

        # 请求新增项目接口，新增一个项目
        projects_url = conf.get('env', 'base_url') + '/projects/'
        projects_params = {
            "name": random_project_name(),
            "leader": "lemonban",
            "tester": "测试人01",
            "programmer": "zhang",
            "publish_app": "123",
            "desc": "测试项目01"
        }
        headers = {'Authorization': cls.token}
        projects_response = requests.request(method='post', url=projects_url, json=projects_params, headers=headers)
        projects_res = projects_response.json()
        # 获取新增项目的项目id
        cls.project_id = jsonpath(projects_res, '$.id')[0]
        # 获取新增项目的项目名称
        cls.pro_name = projects_params['name']

    @myddt.data(*cases_data)
    def test_interface(self, case):
        # 请求url
        url = conf.get('env', 'base_url') + case['url']
        # 请求参数
        params = eval(replace_data(case['data'], TestInterface))
        # 请求头
        headers = {'Authorization': self.token}
        # 请求方法
        method = case['method']
        # 预期结果
        expected = eval(replace_data(case['expected'], TestInterface))
        # 实际结果
        response = requests.request(method='post', url=url, json=params, headers=headers)
        res = response.json()

        print('预期结果：', expected)
        print('实际结果：', res)

        try:
            self.assertEqual(response.status_code, case['code'])
            assert_dict_item(expected, res)
        except AssertionError as e:
            log.exception(e)
            log.error('用例{}，执行未通过'.format(case['title']))
            self.excel.write_excel(row=case['case_id'] + 1, column=9, value='未通过')
            raise e
        else:
            log.info('用例{}，执行通过'.format(case['title']))
            self.excel.write_excel(row=case['case_id'] + 1, column=9, value='通过')
