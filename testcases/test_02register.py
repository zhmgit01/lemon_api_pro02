# -*- coding:utf-8 -*-
# @FileName  :test_02register.py
# @Time      :2020/9/14 15:22
# @Author    :zhm
"""
测试注册接口
"""

import os
import unittest
import requests
from common import myddt
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_log import log
from common.handle_data import replace_data
from tools.tools import random_name, assert_dict_item


@myddt.ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel(file_name=os.path.join(DATA_DIR, 'apicases.xlsx'), sheet_name='register')
    cases_data = excel.read_excel()

    def setUp(self):
        TestRegister.name = random_name()

    @myddt.data(*cases_data)
    def test_register(self, case):
        # 请求url
        register_url = conf.get('env', 'base_url') + case['url']
        # 请求参数
        case['data'] = replace_data(case['data'], TestRegister)
        params = eval(case['data'])
        # 请求方法
        method = case['method']
        # 预期结果
        expected = eval(replace_data(case['expected'], TestRegister))
        # 实际结果
        response = requests.request(method=method, url=register_url, json=params)
        res = response.json()

        print('预期结果：', expected)
        print('实际结果：', res)

        try:
            self.assertEqual(response.status_code, case['code'])
            assert_dict_item(expected, res)
        except AssertionError as e:
            self.excel.write_excel(row=case['case_id'] + 1, column=9, value='未通过')
            log.error('用例{}，执行未通过'.format(case['title']))
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=case['case_id'] + 1, column=9, value='通过')
            log.info('用例{}，执行通过'.format(case['title']))
