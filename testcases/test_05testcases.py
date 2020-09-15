# -*- coding:utf-8 -*-
# @FileName  :test_05testcases.py
# @Time      :2020/9/14 18:25
# @Author    :zhm
"""
测试新增测试用例的接口的用例类
"""

import os
import unittest
import requests
from jsonpath import jsonpath

from common import myddt
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_log import log
from common.handle_config import conf
from common.handle_data import replace_data
from tools.tools import random_project_name, assert_dict_item


@myddt.ddt
class TestTestcases(unittest.TestCase):

    excel = HandleExcel(file_name=os.path.join(DATA_DIR, 'apicases.xlsx'), sheet_name='testcases')
    cases_data = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        """测试执行之前环境的准备"""

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
            "desc": "测试项目"
        }
        headers = {'Authorization': cls.token}
        projects_response = requests.request(method='post', url=projects_url, json=projects_params, headers=headers)
        projects_res = projects_response.json()
        # 获取新增项目的项目id
        cls.project_id = jsonpath(projects_res, '$.id')[0]
        # 获取新增项目的项目名称
        cls.pro_name = projects_params['name']

        # 3、准备添加接口的参数，添加一个接口
        inter_url = conf.get("env", "base_url") + "/interfaces/"
        inter_data = {
            "name": "{}_测试接口".format(projects_params["name"]),
            "project_id": cls.project_id,
            "tester": "zhangzhang",
            "desc": "测试接口01"
        }
        inter_response = requests.request(url=inter_url, method="post", json=inter_data, headers=headers)
        inter_res = inter_response.json()
        # 保存接口id
        cls.interface_id = str(jsonpath(inter_res, "$..id")[0])
        # 保存添加的接口名
        cls.inter_name = inter_data["name"]

    @myddt.data(*cases_data)
    def test_testcases(self, case):
        # 请求url
        url = conf.get('env', 'base_url') + case['url']
        # 请求参数
        params = eval(replace_data(case['data'], TestTestcases))
        # 请求头
        headers = {'Authorization': self.token}
        # 请求方法
        method = case['method']
        # 预期结果
        expected = eval(replace_data(case['expected'], TestTestcases))
        # 实际结果
        response = requests.request(method=method, url=url, json=params, headers=headers)
        res = response.json()

        print('预期结果：', expected)
        print('实际结果：', res)
        # 断言
        try:
            self.assertEqual(response.status_code, case['code'])
            assert_dict_item(expected, res)
        except AssertionError as e:
            log.exception(e)
            log.error('用例{}，执行未通过'.format(case['title']))
            self.excel.write_excel(row=case['case_id'] + 1, column=9, value='未通过')
            raise e
        else:
            log.info('用例{}，执行未通过'.format(case['title']))
            self.excel.write_excel(row=case['case_id'] + 1, column=9, value='未通过')
