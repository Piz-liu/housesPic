#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlrd

# data = xlrd.open_workbook(u'F:\gongxiang\lptp\济南楼盘\楼盘户型图数据导入模板11.5济南.xls')
# data = xlrd.open_workbook(u'F:\gongxiang\lptp\杭州楼盘\杭州楼盘户型图数据导入模板.xls')
data = xlrd.open_workbook(u'F:\gongxiang\lptp\hz.xlsx')
# data = xlrd.open_workbook(u'F:\gongxiang\lptp\jn.xlsx')


sheetIndex = 0
# 获取整个sheet表格
def getExcelTable():
    table = data.sheets()[sheetIndex]
    return table


def getExcelTableNRows():
    table = data.sheets()[sheetIndex]
    return table.nrows

# 获取行
def getExcelRow(row):
    table = getExcelTable()
    return table.row_values(row)


def getExcelCell(start, end):
    table = getExcelTable()
    cell = table.cell(start, end).value
    return cell


def write(value):
    f = open('id.txt', 'a')
    try:
        f.write(str(value) + "\n")
    except TypeError as e:
        print 'error'
        f.write("\n")
    finally:
        f.close()

# for x in range(5):
#     print getExcelCell(0,x+1,1)


