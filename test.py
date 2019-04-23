# -*- coding:utf-8 -*-

import add as add
import my_sqlConnection as mysql
import delete as delete
import ls as ls
import update as update
import help as help
import freeze as freeze
import my_login as login
import admin as admin


"""
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute() 方法执行 SQL 查询
        cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()
        print("Database version : %s " % data)
"""




if __name__ == '__main__':
    print("数据库连接中......")
    db = mysql.createSqlConnection()
    cursor = db.cursor()
    login_word = False
    while 1:
        print("需要验证用户登录")
        print("--------------------------------")
        print("请输入用户名：")
        username = input().strip()
        print("请输入密码：")
        password = input().strip()
        login_word = login.isAdminUser(username, password, cursor)
        if login_word:
            break
    if login_word:
        print("数据库连接成功")
        while 1:
            str = input().strip()
            if str[0:2] == "ls":
                ls.ls_main(cursor, str[2:])
            elif str[0:3] == "add":
                add.add_main(cursor, db, str[3:])
            elif str[0:6] == "delete":
                delete.delete_main(cursor, db, str[6:])
            elif str[0:6] == "update":
                update.update_main(cursor, db, str[6:])
            elif str[0:6] == "freeze":
                freeze.freeze_main(cursor, db, str[6:])
            elif str[0:4] == "help":
                help.helper_main()
            elif str[0:5] == "admin":
                admin.admin_main(cursor, db, str[5:])
            elif str == "exit":
                print("正在退出")
                db.close()
                exit(0)
            else:
                print("暂时没有提供此服务")
                continue
        db.close()

