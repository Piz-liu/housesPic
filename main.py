#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = '500004'
import excelutil
import mongoDb

db_pic = mongoDb.getMongoConn()
db_house = mongoDb.getMongoConn(database='houses')
num = excelutil.getExcelTableNRows()
# pic_path = u'F:\gongxiang\lptp\济南楼盘\houses_type_pic\\'
pic_path = u'F:\gongxiang\lptp\杭州楼盘\houses_type_pic\\'

# 处理float
def switchToStr(row, line):
    title = excelutil.getExcelCell(row, line)
    if isinstance(title, float):
        title = str(int(title))
    if isinstance(title, unicode):
        title = title.split("(")[0]
    return title


# 保存图片
def saveImp(imagePath, name):
    try:
        return mongoDb.putImg(imagePath, db_pic, name)
    except IOError as e:
        e.message
        print(u"图片不存在")
        return None


# 获取楼盘
def findHouses(condition):
    oldHouse = db_house.houses.find_one(condition)
    print oldHouse
    if oldHouse is None:
        # excelutil.write(houseName)
        print condition["name"]
        print(u"没有楼盘数据")
    return oldHouse


# 获取楼盘类型
def getHouseType(oldHouse, condition):
    try:
        oldList = oldHouse["new_houses_type"]
    except KeyError:
        print 'new_houses_type not found,create!'
        db_house.houses.update(condition, {"$set": {"new_houses_type": []}})
        house = findHouses(condition)
        oldList = house["new_houses_type"]
    return oldList


# 新建记录
def saveNewHouseType(house_room, house_hall, house_toilet, house_area, house_type_title, id):
    # 循环完没有找到
    value = {"house_room": house_room, "house_hall": house_hall, "house_toilet": house_toilet,
             "house_area": house_area, "house_type_title": house_type_title, "mongo_key": id}
    db_house.houses.update(condition, {"$push": {"new_houses_type": value}})


for x in range(num):
    row = x + 1
    print row
    if row == num:
        print u'完成表中数据'
        break
    name = excelutil.getExcelCell(row, 8).split("\\")[1].strip()
    print u"图片名:" + name
    imagePath = pic_path + name
    houseName = excelutil.getExcelCell(row, 1)
    city = excelutil.getExcelCell(row, 2)
    house_type_title = switchToStr(row, 3)
    # 室
    house_room = switchToStr(row, 4)
    # 厅
    house_hall = switchToStr(row, 5)
    # 卫
    house_toilet = switchToStr(row, 6)
    # 面积
    house_area = switchToStr(row, 7)
    condition = {"name": houseName, "city": city}
    oldHouse = findHouses(condition)
    if oldHouse is None:
        continue
    oldList = getHouseType(oldHouse, condition)
    # 保存图片
    id = saveImp(imagePath, name)
    saveNewHouseType(house_room, house_hall, house_toilet, house_area, house_type_title, str(id))




# for x in range(num):
#     row = x + 1
#     print row
#     if row == num:
#         print u'完成表中数据'
#         break
#     col = 9
#     name = excelutil.getExcelCell(row, 8).split("\\")[1]
#     print u"图片名:" + name
#     # imagePath = u'F:\gongxiang\lptp\济南楼盘\houses_type_pic\\' + name
#     imagePath = u'F:\gongxiang\lptp\杭州楼盘\houses_type_pic\\' + name
#     # 更新原来数据
#     houseName = excelutil.getExcelCell(row, 1)
#     city = excelutil.getExcelCell(row, 2)
#     house_type_title = excelutil.getExcelCell(row, 3)
#     if isinstance(house_type_title, float):
#         house_type_title = str(int(house_type_title))
#     # 室
#     house_room = excelutil.getExcelCell(row, 4)
#     # 厅
#     house_hall = excelutil.getExcelCell(row, 5)
#     # 卫
#     house_toilet = excelutil.getExcelCell(row, 6)
#     # 面积
#     house_area = excelutil.getExcelCell(row, 7)
#     if isinstance(house_area, unicode):
#         house_area = house_area.split("(")[0]
#     condition = {"name": houseName, "city": city}
#     oldHouse = findHouses(condition)
#     # 保存图片
#     id = saveImp(imagePath, name)
#     if id is None or oldHouse is None:
#         continue
#     oldList = getHouseType(oldHouse)
#     if len(oldList) > 0:
#         for index, value in enumerate(oldList):
#             try:
#                 houseArea = value["house_area"]
#                 houseTypeTitle = value["house_type_title"]
#             except KeyError:
#                 print u"键值不存在 不存在,新建"
#                 saveNewHouseType(house_room, house_hall, house_toilet, house_area, house_type_title, id)
#             key = 'houses_type.%d.' % index
#             set_condi = {
#                 "$set": {key + "mongo_key": id, key + "house_room": house_room,
#                          key + "house_hall": house_hall,
#                          key + "house_toilet": house_toilet}}
#             if house_area:
#                 try:
#                     if houseArea:
#                         if isinstance(houseArea, unicode):
#                             houseArea = houseArea.split(u"㎡")[0]
#                         if int(houseArea) == int(house_area):
#                             if value["house_type_title"]:
#                                 if isinstance(houseTypeTitle, unicode):
#                                     title = houseTypeTitle
#                                 else:
#                                     title = str(houseTypeTitle)
#                                 if house_type_title in title:
#                                     print u'匹配房型成功'
#                                     db_house.houses.update(condition, set_condi)
#                                     continue
#                 except KeyError:
#                     print u"house_area 不存在,新建"
#                 except ValueError:
#                     print u"house_area 包含数字跳过,第" + str(row)
#                     continue
#             elif house_type_title:
#                 try:
#                     # 没有面积 按户型匹配
#                     if houseTypeTitle:
#                         if isinstance(houseTypeTitle, unicode):
#                             title = value["house_type_title"]
#                         else:
#                             title = str(houseTypeTitle)
#                         if house_type_title in title:
#                             db_house.houses.update(condition, set_condi)
#                             continue
#                         print u"house_area 不存在,新建"
#                 except KeyError:
#                     print u"house_area 不存在,新建"
#         print u'没有匹配房型'
#         # 循环完没有找到
#         saveNewHouseType(house_room, house_hall, house_toilet, house_area, house_type_title, id)
#     else:
#         # 一个都不存在
#         saveNewHouseType(house_room, house_hall, house_toilet, house_area, house_type_title, id)
