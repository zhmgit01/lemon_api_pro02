# -*- coding:utf-8 -*-
# @FileName  :run.py
# @Time      :2020/9/14 10:17
# @Author    :zhm

"""
测试主文件
"""
import unittest
from unittestreport import TestRunner
from common.handle_path import CASE_DIR, REPORT_DIR
from common.handle_config import conf


# 加载测试套件
suite = unittest.defaultTestLoader.discover(CASE_DIR)

# 运行测试用例
runner = TestRunner(suite=suite,
                    filename=conf.get('report', 'filename'),
                    report_dir=REPORT_DIR,
                    tester='zhm',
                    desc='测试报告',
                    templates=1).run()
