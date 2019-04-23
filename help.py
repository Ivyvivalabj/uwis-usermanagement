# -*- coding:utf-8 -*-
import pymysql
import hashlib

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
    print("本文档提供简单的帮助：")
    print("1.增加操作：")
    print("\t输入指令格式：add 安装路径(如：d:\\\\test\\\\doc)\n")
    print("2.删除操作")
    print("\t(1)删除指定账号")
    print("\t\t输入指令格式：delete account 账号用户名")
    print("\t(2)删除指定班级，并删除班级下的所有学生，以及学生所对应的用户账号")
    print("\t\t输入指令格式：delete class 某某学校-某某年级-某某班")
    print("\t(3)删除指定班级的所有学生，以及学生所对应的用户账号")
    print("\t\t输入指令格式：delete student 某某学校-某某年级-某某班\n")

    print("3.修改操作")
    print("\t输入指令格式：update 属性名=值/属性名=值,属性名=值(更新多个属性使用逗号分隔) 用户名\n")

    print("4.查询操作")
    print("\t(1)输出一个学校的所有账号")
    print("\t\t输入指令格式：ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） schoolname=学校名称")
    print("\t(2)输出一个地区的所有学校")
    print("\t\t输入指令格式：ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） place=地区名")
    print("\t(3)输出一个班级的所有学生账号")
    print("\t\t输入指令格式：ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） class=某某学校-某某年级-某某班")
    print("\t(4)对某个学生进行查询")
    print("\t\t输入指令格式：ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） username=学生账号\n")

    print("5.账号冻结")
    print("\t(1)冻结指定用户组")
    print("\t\t输入指令格式：freeze usergroup=用户组名字")
    print("\t(2)冻结一个学校的所有用户")
    print("\t\t输入指令格式：freeze school=学校名")
    print("\t(3)冻结一个年级的所有用户")
    print("\t\t输入指令格式：freeze grade=某某学校-某某年级")
    print("\t(4)冻结一个班级的所有用户")
    print("\t\t输入指令格式：freeze class=某某学校-某某年级-某某班级")
