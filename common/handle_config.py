# -*- coding:utf-8 -*-
# @FileName  :handle_config.py
# @Time      :2020/9/14 13:44
# @Author    :zhm

"""
封装配置文件操作类
"""

import os
from configparser import ConfigParser
from common.handle_path import CONFIG_DIR


class HandleConfig(ConfigParser):

    def __init__(self, file_nme, encoding='utf-8'):
        """重写父类的__init__方法"""
        super().__init__()
        self.filename = file_nme
        self.encoding = encoding
        # 读取配置文件的内容
        self.read(filenames=file_nme, encoding=encoding)

    def write_data(self, section, option, value):
        """将数据写入配置文件中"""
        self.set(section=section, option=option, value=value)
        self.write(fp=open(self.filename, 'w', encoding=self.encoding))


conf = HandleConfig(file_nme=os.path.join(CONFIG_DIR, 'config.ini'))
