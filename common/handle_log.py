# -*- coding:utf-8 -*-
# @FileName  :handle_log.py
# @Time      :2020/9/14 11:28
# @Author    :zhm

"""
封装日志操作模块
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from common.handle_config import conf
from common.handle_path import LOG_DIR


class HandleLog:

    @staticmethod
    def create_log():
        # 创建日志收集器
        logger = logging.getLogger('test')
        # 设置日志收集器的等级
        logger.setLevel(conf.get('logging', 'level'))

        # 创建日志输出渠道
        # 1、创建输入到控制台的输出渠道
        sh = logging.StreamHandler()
        # 设置输出渠道的输出等级
        sh.setLevel(conf.get('logging', 'sh_level'))
        # 将输出渠道添加到收集器中
        logger.addHandler(sh)
        # 2、创建输入到文件的数据渠道
        fh = TimedRotatingFileHandler(filename=os.path.join(LOG_DIR, conf.get('logging', 'log_name')),
                                      encoding='utf-8',
                                      backupCount=7,
                                      when='d',
                                      interval=1)
        # 设置输出渠道的输出等级
        fh.setLevel(conf.get('logging', 'fh_level'))
        # 将输出渠道添加到收集器中
        logger.addHandler(fh)

        # 设置日志输出格式
        formatter = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        mat = logging.Formatter(formatter)

        # 设置日志输出的日志显示格式
        fh.setFormatter(mat)
        sh.setFormatter(mat)

        return logger


# 实例化log对象，其他模块在引用时，导入该对象，保证在程序运行过程中，只存在一个 日志 对象，避免出现日志重复记录的问题
log = HandleLog.create_log()
