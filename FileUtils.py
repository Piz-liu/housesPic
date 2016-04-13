#! /usr/env python
# -*- coding:utf-8 -*-

import os

import os.path

import mongoDb
import excelutil

rootdir = u"F:\gongxiang\lptp\杭州楼盘\houses_pic"  # 指明被遍历的文件夹
cityNmae = u"杭州"
# rootdir = u"F:\gongxiang\lptp\济南楼盘\houses_pic"  # 指明被遍历的文件夹
# cityNmae = u"济南"
db_house = mongoDb.getMongoConn(database='houses')
db_pic = mongoDb.getMongoConn()
jt = None
sj = None
xg = None
pt = None
yb = None


def getFilePath(root):
    result_path = []
    for parent, dirnames, filenames in os.walk(root):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for dirname in dirnames:  # 输出文件夹信息
            # print "parent is:" + parent
            # print "dirname is" + dirname
            result_path.append(os.path.join(parent, dirname))
    return result_path  # ,result_path_All


def getFile(root):
    result_path_All = []
    for parent, dirnames, filenames in os.walk(root):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            # print "parent is:" + parent
            # print "filename is:" + filename
            # print "the full name of the file is:" + os.path.join(parent,filename) # 输出文件路径信息
            # result_path.append(parent)
            result_path_All.append(os.path.join(parent, filename))
    return result_path_All


def savePicToMongo(arr, typeNme, type, condition):
    if not arr:
        print typeNme + u" 该类型暂无图片"
        return
    house = db_house.houses.find_one(condition)
    if house:
        for value in arr:
            picname = value.split("\\")[-1]
            # 存 mongo 返回KEY
            key = mongoDb.putImg(value, db_pic, picname)
            pic_dic = {"type_name": typeNme, "type": type, "mongoKey": str(key)}
            db_house.houses.update(condition, {"$push": {"houses_pic": pic_dic}})
            print u"写入成功"
    else:
        print condition["name"]
        print u"没有找到数据"


rootPath = getFilePath(rootdir)

num = excelutil.getExcelTableNRows()

# [608,609,610,611,612]
for x in range(num):
    print x
    name = excelutil.getExcelCell(x, 0).replace(' ', '')
    for index, value in enumerate(rootPath):
        if name in value:
            val = value.split("\\")[-1]
            if val == u"交通图":
                jt = getFile(value)
            if val == u"实景图":
                sj = getFile(value)
            if val == u"效果图":
                xg = getFile(value)
            if val == u"配套图":
                pt = getFile(value)
            if val == u"样板间":
                yb = getFile(value)
    cityNmae = excelutil.getExcelCell(x, 1).replace(' ', '')
    condition = {"name": name, "city": cityNmae}
    jt_keys = savePicToMongo(jt, u"交通图", "2", condition)
    sj_keys = savePicToMongo(sj, u"实景图", "3", condition)
    xg_keys = savePicToMongo(xg, u"效果图", "1", condition)
    pt_keys = savePicToMongo(pt, u"配套图", "5", condition)
    yb_keys = savePicToMongo(yb, u"样板间", "4", condition)
