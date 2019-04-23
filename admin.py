import pymysql
import hashlib
import sys

"""
    需求：读取指定文件后，对指定用户进行identification属性设置（设置为admin）
         如果用户不存在，则需要先创建用户
         admin 文件路径

"""


# def admin_main(cursor,db, des):
#     path = des.strip()
#     # path = 'test.txt'
#     with open(path, 'r') as f:
#         lineList = f.readlines()
#         print(lineList)
#         for line in lineList:
#             username = line.strip()
#             sql = "SELECT identification,id FROM yzbc.yz_user where username = '%s'" % (username)
#             cursor.execute(sql)
#             result = cursor.fetchone()
#             if result:
#                 identi = result[0]
#                 uid = result[1]
#                 if identi == 'admin':
#                     print("当前用户已经是admin，不需要更新")
#                 else:
#                     sql = "UPDATE yzbc.yz_user SET identification = '%s' WHERE id = %s;"
#                     data = (identi, uid)
#                     try:
#                         # 执行sql语句
#                         cursor.execute(sql % data)
#                         # 提交到数据库执行
#                         db.commit()
#                         print("admin权限更新已提交到数据库")
#                     except:
#                         print("写入发生错误，进行数据回滚")
#                         db.rollback()
#                         return False
#             else:
#                 print("找不到对应的账号信息")



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

    path = sys.argv[1]
    with open(path, 'r') as f:
        lineList = f.readlines()
        print(lineList)
        for line in lineList:
            username = line.strip()
            sql = "SELECT identification,id FROM yzbc.yz_user where username = '%s'" % (username)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                identi = result[0]
                uid = result[1]
                if identi == 'admin':
                    print("当前用户已经是admin，不需要更新")
                else:
                    sql = "UPDATE yzbc.yz_user SET identification = '%s' WHERE id = %s;"
                    data = (identi, uid)
                    try:
                        # 执行sql语句
                        cursor.execute(sql % data)
                        # 提交到数据库执行
                        db.commit()
                        print("admin权限更新已提交到数据库")
                    except:
                        print("写入发生错误，进行数据回滚")
                        db.rollback()
            else:
                print("找不到对应的账号信息")
