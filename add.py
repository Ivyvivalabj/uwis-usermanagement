# -*- coding:utf-8 -*-
import os as os
import my_add_feizhixia as fzx
import my_add_zhixia as zx
import pymysql
import hashlib
import sys



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
    print(sys.argv[0:])
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
        f = open('pwd.txt','w+')
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
                f.write(username+"\n")
                f.write(password)
                break
    des = sys.argv[1]
    zhixia = ['北京市', '天津市', '上海市', '重庆市']
    des = des.strip()
    path = des
    print("正在检测安装文件是否齐全...........")
    # 判断是否是直辖市，判断后执行对应的方法
    if os.scandir(path):
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir() and entry.name != "logs" and entry != None:
                    if entry.name in zhixia:
                        zx.zhixia_main(entry, path, db, cursor)
                    else:
                        fzx.feizhixia_main(entry, path, db, cursor)
    # 如果当前的路径不存在，则提示用户当前路径不存在
    else:
        print("当前路径不存在")


