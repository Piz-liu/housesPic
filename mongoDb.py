#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = '500004'
from cStringIO import StringIO

import pymongo
from gridfs import *
from bson.objectid import ObjectId

host = '127.0.0.1'  # "172.16.10.35"
port = 27017
database = u'hw-sq'


def getMongoConn(host=host, port=port, database=database):
    # conn = pymongo.Connection("127.0.0.1",27017)
    conn = pymongo.Connection(host, port)
    # 连接库
    database = conn[database]
    # 用户认证
    # db.authenticate('','')
    return database


def putImg(imagePath, db, filename):
    with open(imagePath, 'rb') as f:
        fs = GridFS(db, 'fs')
        suffix = filename.split('.')[1]
        content = StringIO(f.read())
        x = fs.put(content.getvalue(), filename=filename, contentType='image/' + suffix)
        print x
        return x


# 获得图片
def get(id):
    db = getMongoConn()
    gf = None
    try:
        gf = db.get(ObjectId(id))
        im = gf.read()  # read the data in the GridFS
        dic = {}
        dic["chunk_size"] = gf.chunk_size
        dic["metadata"] = gf.metadata
        dic["length"] = gf.length
        dic["upload_date"] = gf.upload_date
        dic["name"] = gf.name
        dic["content_type"] = gf.content_type
        dic["format"] = gf.format
        return (im, dic)
    except Exception, e:
        print e
        return (None, None)
    finally:
        if gf:
            gf.close()


# 将gridFS中的图片文件写入硬盘
def write_2_disk( data, dic):
    name = "./get_%s" % dic['name']




# host = "172.16.10.35"
# port = 27017
# db = getMongoConn()
# id = "ObjectId('5642b793e8917b22a8000000')"
# value = db.fs.files.find_one({"_id": id})
# print value
# db.fs.files.update({"_id": id}, {"$set":{'kkk':'123'}})
# x = db.fs.files.find()
# for i in x:
#  print i
# db.user.save({'id':1,'name':'kaka','sex':'male'})
