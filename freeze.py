# -*- coding:utf-8 -*-
import pymysql
import hashlib
import sys
"""
需求：
    1.冻结指定用户组
    freeze usergroup=用户组名字
    2.冻结指定用户
    freeze usergroup=用户组名字
    3.冻结一个学校的所有用户
    freeze school=学校名
    4.冻结一个年级的所有用户
    freeze grade=某某学校-某某年级
    5.冻结一个班级的所有用户
    freeze class=某某学校-某某年级-某某班级
"""


# 冻结指定年级的所有用户账号
def freezeGrade(cursor, db, des):
    desList = des.split('-')
    schoolName = desList[0]
    gradeName = desList[1]
    new_quanxian = ''
    # 通过拼接得到一部分用户组名称
    userGroupName = schoolName + gradeName
    sql = "SELECT quanxian,id FROM yzbc.yz_usergroup where usergroupname like '%%%%%s%%%%' " % (userGroupName)
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for it in result:
            # 第二步：将可登陆权限从权限中去除，并更新用户权限
            quanxianList = it[0]
            groupId = it[1]
            quanxian = quanxianList.split(',')
            for item in quanxian:
                if item == 'login':
                    pass
                else:
                    new_quanxian = new_quanxian + item + ','
            sql = "UPDATE yzbc.yz_usergroup SET quanxian = '%s' WHERE id = %s;"
            data = (new_quanxian, groupId)
            try:
                # 执行sql语句
                cursor.execute(sql % data)
                # 提交到数据库执行
                db.commit()
                print("账号冻结已提交到数据库")
            except:
                print("写入发生错误，进行数据回滚")
                db.rollback()
                return False
    else:
        print("找不到对应的账号信息")


# 冻结指定学校的所有用户账号
def freezeSchool(cursor, db, des):
    schoolName = des
    # 通过拼接得到一部分用户组名称
    sql = "SELECT quanxian,id FROM yzbc.yz_usergroup where usergroupname like '%%%%%s%%%%' " % (schoolName)
    cursor.execute(sql)
    result = cursor.fetchall()
    new_quanxian = ''
    if result:
        for it in result:
            # 第二步：将可登陆权限从权限中去除，并更新用户权限
            quanxianList = it[0]
            groupId = it[1]
            quanxian = quanxianList.split(',')
            for item in quanxian:
                if item == 'login':
                    pass
                else:
                    new_quanxian = new_quanxian + item + ','
            sql = "UPDATE yzbc.yz_usergroup SET quanxian = '%s' WHERE id = %s;"
            data = (new_quanxian, groupId)
            try:
                # 执行sql语句
                cursor.execute(sql % data)
                # 提交到数据库执行
                db.commit()
                print("账号冻结已提交到数据库")
            except:
                print("写入发生错误，进行数据回滚")
                db.rollback()
                return False
    else:
        print("找不到对应的账号信息")


# 冻结指定班级的所有用户账号
def freezeClass(cursor, db, des):
    desList = des.split('-')
    schoolName = desList[0]
    gradeName = desList[1]
    className = desList[2]
    new_quanxian = ''
    # 通过拼接得到一部分用户组名称
    userGroupName = schoolName + gradeName + className
    sql = "SELECT quanxian,id FROM yzbc.yz_usergroup where usergroupname like '%%%%%s%%%%' " % (userGroupName)
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for it in result:
            # 第二步：将可登陆权限从权限中去除，并更新用户权限
            quanxianList = it[0]
            groupId = it[1]
            quanxian = quanxianList.split(',')
            for item in quanxian:
                if item == 'login':
                    pass
                else:
                    new_quanxian = new_quanxian + item + ','
            sql = "UPDATE yzbc.yz_usergroup SET quanxian = '%s' WHERE id = %s;"
            data = (new_quanxian, groupId)
            try:
                # 执行sql语句
                cursor.execute(sql % data)
                # 提交到数据库执行
                db.commit()
                print("账号冻结已提交到数据库")
            except:
                print("写入发生错误，进行数据回滚")
                db.rollback()
                return False
    else:
        print("找不到对应的账号信息")


# 冻结指定用户组的用户账号
def freezeUserGroup(cursor, db, des):
    username = des.strip(' ')
    new_quanxian = ''
    # 第一步：通过用户名，获取用户权限
    sql = "SELECT quanxian FROM yzbc.yz_usergroup where usergroupname = '%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        # 第二步：将可登陆权限从权限中去除，并更新用户权限
        quanxianList = result[0]
        quanxian = quanxianList.split(',')
        for it in quanxian:
            if it == 'login':
                pass
            else:
                new_quanxian = new_quanxian + it + ','
        sql = "UPDATE yzbc.yz_usergroup SET quanxian = '%s' WHERE usergroupname = '%s';"
        data = (new_quanxian, username)
        try:
            # 执行sql语句
            cursor.execute(sql % data)
            # 提交到数据库执行
            db.commit()
            print("账号冻结已提交到数据库")
        except:
            print("写入发生错误，进行数据回滚")
            db.rollback()
            return False
    else:
        print("找不到对应的账号信息")


def freeze_main(cursor, db, des):
    des = des.strip()
    desList = des.split(' ')
    print(desList)
    if desList.__len__() > 1:
        print("用户输入错误，请按照要求进行输入")
        return
    else:
        desList2 = desList[0].split('=')
        print(desList2)
        if desList2[0] == 'class':
            freezeClass(cursor, db, desList2[1])
        elif desList2[0] == 'usergroup':
            freezeUserGroup(cursor, db, desList2[1])
        elif desList2[0] == 'school':
            freezeSchool(cursor, db, desList2[1])
        elif desList2[0] == 'grade':
            freezeGrade(cursor, db, desList2[1])
        else:
            print("暂时没有提供这项服务")


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
        # exit()
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
    if sys.argv.__len__() > 2:
        print("用户输入错误，请按照要求进行输入")

    else:
        desList2 = sys.argv[1].split('=')
        print(desList2)
        if desList2[0] == 'class':
            freezeClass(cursor, db, desList2[1])
        elif desList2[0] == 'usergroup':
            freezeUserGroup(cursor, db, desList2[1])
        elif desList2[0] == 'school':
            freezeSchool(cursor, db, desList2[1])
        elif desList2[0] == 'grade':
            freezeGrade(cursor, db, desList2[1])
        else:
            print("暂时没有提供这项服务")