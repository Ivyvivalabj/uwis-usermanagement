# -*- coding:utf-8 -*-

import pymysql
def createSqlConnection():
    location = "120.26.47.132"
    username = "robotweb"
    password = "LG5qnmHfe5KmVDQb"
    database = "yzbc"
    # 打开数据库连接
    try:
        db = pymysql.connect(location, username, password, database, charset='utf8')
        return db
    except:
        print("数据库连接失败")
        return False


