# -*- coding:utf-8 -*-
# @FileName  :handle_data.py
# @Time      :2020/9/14 14:15
# @Author    :zhm

"""
封装替换用例参数的方法
"""

import re
from common.handle_config import conf


def replace_data(data, cls):
    """替换用例参数"""
    # re.search("#(.+?)#", data) 无与此匹配的的内容，则返回 None
    while re.search("#(.+?)#", data):
        item = re.search("#(.+?)#", data)
        # 需要替换的数据
        # 返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。
        rep_data = item.group()
        # 要替换的属性
        # 获得组内的匹配项
        key = item.group(1)
        try:
            value = conf.get('test_data', key)
        except:
            value = getattr(cls, key)
        data = data.replace(rep_data, str(value))
    return data
