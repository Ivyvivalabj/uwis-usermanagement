# -*- coding:utf-8 -*-

import pymysql
import hashlib
import sys
from xml.dom.minidom import parse
import xml.dom.minidom

"""
需求：
    1.修改指定学生的账号,设置账号的权限等级,设置账号的使用期限，设置账号的勋章
    update 属性名=值/属性名=值,属性名=值(更新多个属性使用逗号分隔) 用户名
"""

def isAdminUser(username, password, cursor):
    sql = "SELECT password,identification FROM yzbc.yz_user where username = '%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
       #  验证当前用户的identification是否为admin
        if result[1] == 'admin':
            psw = result[0]
            hash = hashlib.md5()  # md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
            hash.update(bytes(password, encoding='utf-8'))  # 要对哪个字符串进行加密，就放这里
            psw_md5 = hash.hexdigest()
            if psw == psw_md5:
                return True
            else:
                print("您输入的密码有误，请确认后再输入")
                return False

        else:
           print("您没有权限进入用户管理界面")
           return False

    else:
        return False
        print("找不到对应的账号信息")


if __name__ == '__main__':
    location = "120.26.47.132"
    username = "robotweb"
    password = "LG5qnmHfe5KmVDQb"
    database = "yzbc"
    # 打开数据库连接
    try:
        db = pymysql.connect(location, username, password, database, charset='utf8')
    except:
        print("数据库连接失败")
        exit()
    cursor = db.cursor()
    login_word = False
    try:
        f = open('pwd.txt')
        userInfor = f.readlines()
        usrname = userInfor[0].strip()
        pwd = userInfor[1].strip()
        login_word = isAdminUser(usrname, pwd, cursor)
        if login_word == False:
            print("当前管理员用户已经更新，请重新登录")
            while 1:
                print("需要验证用户登录")
                print("--------------------------------")
                print("请输入用户名：")
                usernameRe = input().strip()
                print("请输入密码：")
                passwordRe = input().strip()
                login_word = isAdminUser(usernameRe, passwordRe, cursor)
                if login_word:
                    print("数据库登录成功")
                    # 将用户名和密码写入pwd.txt文件，文件中第一行写用户名；第二行写密码
                    f.write(usernameRe + "\n")
                    f.write(passwordRe)
                    break
    except:
        # 如果保存的文件不存在，则创建文件，并要求用户输入账户名和密码
        f = open('pwd.txt', 'w+')
        while 1:
            print("需要验证用户登录")
            print("--------------------------------")
            print("请输入用户名：")
            username = input().strip()
            print("请输入密码：")
            password = input().strip()
            login_word = isAdminUser(username, password, cursor)
            if login_word:
                print("数据库登录成功")
                # 将用户名和密码写入pwd.txt文件，文件中第一行写用户名；第二行写密码
                f.write(username + "\n")
                f.write(password)
                break
    # 遍历配置文件，进行各属性的配置
    # logG = 1时将日志输出打开，logG = 0时关闭日志
    logG = 0
    DOMTree = xml.dom.minidom.parse("config.xml")
    services = DOMTree.documentElement
 
    # 在集合中获取所有电影
    service = services.getElementsByTagName("update")
    
    for attrs in service:
        attr = attrs.getElementsByTagName('log')[0]
        logG = attr.childNodes[0].data
    desList = sys.argv
    print(desList)
    if desList.__len__() > 3:
        if logG:
            print("用户输入错误")
    else:
        attrList = desList[1]
        condition = desList[2]
        attrs = attrList.split(',')
        str = ''
        for i in range(attrs.__len__()):
            itList = attrs[i].split('=')
            # 更新的属性是密码
            if itList[0] == 'password':
                tmp = itList[1]
                m = hashlib.md5()
                b = tmp.encode(encoding='utf-8')
                m.update(b)
                tmp_md5 = m.hexdigest()
                psw = 'password=' + '\'' + tmp_md5 + '\''
                attrs[i] = psw
                if i == attrs.__len__() - 1:
                    str = str + attrs[i].__str__()
                else:
                    str = str + attrs[i].__str__() + ','
            # 更新的属性是昵称
            elif itList[0] == 'nickname':
                tmp = 'nickname=' + '\'' + itList[1] + '\''
                if i == attrs.__len__() - 1:
                    str = str + tmp
                else:
                    str = str + tmp + ','
            # 更新的属性是权限
            elif itList[0] == 'quanxian':
                tmp = 'quanxian=' + '\'' + itList[1] + '\''
                if i == attrs.__len__() - 1:
                    str = str + tmp
                else:
                    str = str + tmp + ','
            # 更新的属性是用户名
            elif itList[0] == 'username':
                tmp = 'username=' + '\'' + itList[1] + '\''
                if i == attrs.__len__() - 1:
                    str = str + tmp
                else:
                    str = str + tmp + ','
            else:
                if i == attrs.__len__() - 1:
                    str = str + attrs[i].__str__()
                else:
                    str = str + attrs[i].__str__() + ','
    
        sql = "UPDATE yzbc.yz_user SET %s WHERE username = '%s';"
        data = (str, condition)
        try:
            # 执行sql语句
            cursor.execute(sql % data)
            # 提交到数据库执行
            db.commit()
            if logG:
                print("用户更新已提交到数据库")
        except:
            if logG:
                print("写入发生错误，进行数据回滚")
            db.rollback()