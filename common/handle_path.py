# -*- coding:utf-8 -*-
# @FileName  :handle_path.py
# @Time      :2020/9/14 10:17
# @Author    :zhm

"""
封装项目中的基本路径
"""

import os

# 项目基本路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 公共文件路径
COMMON_DIR =os.path.join(BASE_DIR, 'common')
# 配置文件路径
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
# 用例文件路径
DATA_DIR = os.path.join(BASE_DIR, 'data')
# 日志文件路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')
# 报告文件路径
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
# 测试用例路径
CASE_DIR = os.path.join(BASE_DIR, 'testcases')
