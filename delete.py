# -*- coding:utf-8 -*-
import pymysql
import hashlib
import sys
from xml.dom.minidom import parse
import xml.dom.minidom
"""
需求：
    1.删除指定账号
    del account 3180702009
    2.删除指定班级，并删除班级下的所有学生，以及学生所对应的用户账号
    del class 某某学校-某某年级-某某班
    3.删除指定班级的所有学生，以及学生所对应的用户账号
    del student 某某学校-某某年级-某某班
"""

# 删除指定班级下的所有学生，以及学生所对应的账号
def delStuandUserByClassName(logG,condition, cursor, db):
    nameList = condition.split('-')
    if nameList.__len__() < 3:
        print("所输入的班级名称格式错误，请按照 某某学校-某某年级-某某班级 的格式输入班级名称")
        return False
    else:
        schoolName = nameList[0]
        gradeName = nameList[1]
        className = nameList[2]
        sql = "SELECT id FROM yzbc.yz_jxgl_school where schoolname = '%s' " % (schoolName)
        cursor.execute(sql)
        schoolData = cursor.fetchone()
        if schoolData:
            schoolId = schoolData[0]
            sql = "SELECT id FROM yzbc.yz_jxgl_grade where schoolid = %s and gradename = '%s'" % (schoolId, gradeName)
            cursor.execute(sql)
            gradeData = cursor.fetchone()
            if gradeData:
                gradeId = gradeData[0]
                sql = "SELECT id,readsortid FROM yzbc.yz_jxgl_class where gradeid = %s and classname = '%s'" % (
                gradeId, className)
                cursor.execute(sql)
                classData = cursor.fetchone()
                if classData:
                    classId = classData[0]
                    classRSId = classData[1]
                    sql = "SELECT uid,id FROM yzbc.yz_jxgl_student where classid = %s " % (classId)
                    cursor.execute(sql)
                    stuData = cursor.fetchall()
                    if stuData:
                        for stu in stuData:
                            # 先把学生表中的用户删除了
                            stuId = stu[1]
                            sql = "DELETE FROM yzbc.yz_jxgl_student WHERE id = %s;" % stuId
                            try:
                                # 执行SQL语句
                                cursor.execute(sql)
                                # 提交修改
                                db.commit()
                            except:
                                print("删除学生%s失败" % stuId)
                                # 发生错误时回滚
                                db.rollback()

                            # 再把用户表中对应的学生账户删除了
                            uid = stu[0]
                            sql = "DELETE FROM yzbc.yz_user WHERE id = %s;" % uid
                            try:
                                # 执行SQL语句
                                cursor.execute(sql)
                                # 提交修改
                                db.commit()
                            except:
                                print("删除用户%s失败" % uid)
                                # 发生错误时回滚
                                db.rollback()
                else:
                    print("您所查询的班级不存在，请确认您的输入是否正确")
            else:
                print("您所查询的年级不存在，请确认您的输入是否正确")
        else:
            print("您所查询的学校不存在，请确认您的输入是否正确")


# 删除指定班级,并删除班级下的学生以及学生账号
def delClassByClassName(condition, cursor, db):
    nameList = condition.split('-')
    if nameList.__len__() < 3:
        print("所输入的班级名称格式错误，请按照 某某学校-某某年级-某某班级 的格式输入班级名称")
        return False
    else:
        schoolName = nameList[0]
        gradeName = nameList[1]
        className = nameList[2]
        sql = "SELECT id FROM yzbc.yz_jxgl_school where schoolname = '%s' " % (schoolName)
        cursor.execute(sql)
        schoolData = cursor.fetchone()
        if schoolData:
            schoolId = schoolData[0]
            sql = "SELECT id FROM yzbc.yz_jxgl_grade where schoolid = %s and gradename = '%s'" % (schoolId, gradeName)
            cursor.execute(sql)
            gradeData = cursor.fetchone()
            if gradeData:
                gradeId = gradeData[0]
                sql = "SELECT id,readsortid FROM yzbc.yz_jxgl_class where gradeid = %s and classname = '%s'" % (gradeId, className)
                cursor.execute(sql)
                classData = cursor.fetchone()
                if classData:
                    classId = classData[0]
                    classRSId = classData[1]
                    sql = "SELECT uid,id FROM yzbc.yz_jxgl_student where classid = %s " % (classId)
                    cursor.execute(sql)
                    stuData = cursor.fetchall()
                    if stuData:
                        for stu in stuData:
                            # 先把学生表中的用户删除了
                            stuId = stu[1]
                            sql = "DELETE FROM yzbc.yz_jxgl_student WHERE id = %s;" % stuId
                            try:
                                # 执行SQL语句
                                cursor.execute(sql)
                                # 提交修改
                                db.commit()
                            except:
                                print("删除学生%s失败" % stuId)
                                # 发生错误时回滚
                                db.rollback()

                            # 再把用户表中对应的学生账户删除了
                            uid = stu[0]
                            sql = "DELETE FROM yzbc.yz_user WHERE id = %s;" % uid
                            try:
                                # 执行SQL语句
                                cursor.execute(sql)
                                # 提交修改
                                db.commit()
                            except:
                                print("删除用户%s失败" % uid)
                                # 发生错误时回滚
                                db.rollback()
                    # 然后再进行班级所对应的板块的删除
                    sql = "DELETE FROM yzbc.yz_readsort WHERE id = %s;" % classRSId
                    try:
                        # 执行SQL语句
                        cursor.execute(sql)
                        # 提交修改
                        db.commit()
                    except:
                        print("删除板块%s失败" % classRSId)
                        # 发生错误时回滚
                        db.rollback()
                    # 然后是进行班级表中对应班级的删除
                    sql = "DELETE FROM yzbc.yz_jxgl_class WHERE id = %s;" % classId
                    try:
                        # 执行SQL语句
                        cursor.execute(sql)
                        # 提交修改
                        db.commit()
                    except:
                        print("删除班级%s失败" % classId)
                        # 发生错误时回滚
                        db.rollback()
                else:
                    print("您所查询的班级不存在，请确认您的输入是否正确")
            else:
                print("您所查询的年级不存在，请确认您的输入是否正确")
        else:
            print("您所查询的学校不存在，请确认您的输入是否正确")


# 根据用户名删除指定账号
def delAccountByUsername(condition, cursor, db):
    sql = "SELECT id FROM yzbc.yz_user where username = '%s';"
    print(sql % condition)
    cursor.execute(sql % condition)
    result = cursor.fetchone()
    uid = 0
    if result:
        uid = result[0]
    else:
        print("您输入的用户名不存在，请确认输入无误后，再次进行操作")
        return False
    sql = "DELETE FROM yzbc.yz_user WHERE username = '%s';" % condition
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        print("删除用户%s成功",condition)
    except:
        # 发生错误时回滚
        db.rollback()

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
    # 遍历配置文件，进行各属性的配置
    # logG = 1时将日志输出打开，logG = 0时关闭日志
    logG = 0
    DOMTree = xml.dom.minidom.parse("config.xml")
    services = DOMTree.documentElement
 
    # 在集合中获取所有电影
    service = services.getElementsByTagName("delete")
    
    for attrs in service:
        attr = attrs.getElementsByTagName('log')[0]
        logG = attr.childNodes[0].data
    attributes = sys.argv[1]
    condition = sys.argv[2]
    # 删除指定账号
    if attributes == 'account':
        delAccountByUsername(logG,condition, cursor, db)
    # 删除指定班级
    elif attributes == 'class':
        delClassByClassName(logG,condition, cursor, db)
    # 删除指定班级的所有学生
    elif attributes == 'student':
        delStuandUserByClassName(logG,condition, cursor, db)
    else:
        print("用户输入错误，请按照要求进行输入")
