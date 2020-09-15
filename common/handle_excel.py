# -*- coding:utf-8 -*-
# @FileName  :handle_excel.py
# @Time      :2020/9/14 10:26
# @Author    :zhm
"""
excel文件操作类
"""
import os
import openpyxl
from common.handle_path import DATA_DIR


class HandleExcel:

    def __init__(self, file_name, sheet_name):
        """
        输出化方法，传入文件名和sheet名
        """
        self.file_name = file_name
        self.sheet_name = sheet_name

    def open(self):
        """封装打开文件方法"""
        # 获取workbook对象
        self.wb = openpyxl.load_workbook(self.file_name)
        # 获取sheetname对象
        self.sh = self.wb[self.sheet_name]

    def read_excel(self):
        """读取excel文件"""
        # 调用实例方法open()
        self.open()
        # 获取sheetname的所有数据行
        res = list(self.sh.rows)
        # 封装第一行的title内容
        title = []
        for c in res[0]:
            title.append(c.value)
        # 封装用例数据内容
        case_data = []
        for row in res[1:]:
            data = []
            for i in row:
                data.append(i.value)
            # 使用聚合函数封装测试数据
            case = dict(zip(title, data))
            case_data.append(case)
        return case_data

    def write_excel(self, row, column, value):
        """封装写入excel文件方法"""
        # 调用实例方法open()
        self.open()
        # 写入文件
        self.sh.cell(row=row, column=column, value=value)
        # 保存写入内容到文件中
        self.wb.save(self.file_name)


if __name__ == '__main__':
    excel = HandleExcel(file_name=os.path.join(DATA_DIR, 'apicases.xlsx'), sheet_name='login')
    print(excel.read_excel())
    # print(excel.write_excel())
