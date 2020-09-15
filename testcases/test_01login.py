# -*- coding:utf-8 -*-
# @FileName  :test_01login.py
# @Time      :2020/9/14 14:28
# @Author    :zhm
"""
测试登录接口
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
from tools.tools import assert_dict_item


@myddt.ddt
class TestLogin(unittest.TestCase):
    excel = HandleExcel(file_name=os.path.join(DATA_DIR, 'apicases.xlsx'), sheet_name='login')
    cases_data = excel.read_excel()

    @myddt.data(*cases_data)
    def test_login(self, case):
        # 请求接口url
        login_url = conf.get('env', 'base_url') + case['url']
        # 请求参数
        case['data'] = replace_data(case['data'], TestLogin)
        params = eval(case['data'])
        # 请求方法
        method = case['method']
        # 预期结果
        expected = eval(case['expected'])
        # 请求接口
        response = requests.request(method=method, url=login_url, json=params)
        res = response.json()

        print('预期结果：', expected)
        print('实际结果：', res)
        # 断言
        try:
            self.assertEqual(response.status_code, case['code'])
            assert_dict_item(expected, res)
        except AssertionError as e:
            log.exception(e)
            self.excel.write_excel(row=case['case_id']+1, column=9, value='未通过')
            log.error('用例{}，执行未通过'.format(case['title']))
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=case['case_id']+1, column=9, value='通过')
            log.info('用例{}，执行通过'.format(case['title']))
