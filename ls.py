# -*- coding:utf-8 -*-

import pymysql
import hashlib
import sys
import os
import csv

# md5解密

"""
需求：
    最大前提：需要支持通配符
    1.输出一个学校的所有账号
    ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） schoolname=学校名称
    2.输出一个地区的所有学校
    ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） place=地区名
    3.输出一个班级的所有学生账号
    ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） class=某某学校-某某年级-某某班级
    4.对某个学生进行查询
    ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） username=学生账号
    5.输出指定姓名（nickname）的所有用户信息，如果有重复，就把所有的输出来
    ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） name=姓名
    
    6.查询账号有效时间
    
    7.输出一个年级的所有账号
    ls 属性名/*(所有属性)/属性名,属性名（多个属性使用逗号分隔） grade=某某学校-某某年级

"""
# 输出一个年级的所有账号
def findAllStudentByGradeName(attributes,gradeName, cursor):
    nameList = gradeName.split('-')
    if nameList.__len__() != 2:
        print("所输入的班级名称格式错误，请按照 某某学校-某某年级 的格式输入班级名称")
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
                sql = "SELECT uid FROM yzbc.yz_jxgl_student where gradeid = %s" % (gradeId)
                cursor.execute(sql)
                stuData = cursor.fetchall()
                if stuData:
                    result = []
                    cols = []
                    for stu in stuData:
                        uid = stu[0]
                        sql = "SELECT %s FROM yzbc.yz_user where id = %s" % (attributes, uid)
                        cursor.execute(sql)
                        userData = cursor.fetchone()
                        cols = cursor.description
                        result.append(userData)
                    print("%s的所有学生账号详细情况如下：" % className)
                    colsList = []
                    for col in cols:
                        colsList.append(col[0])
                    for user in result:
                        resultContent = ""
                        for i in range(colsList.__len__()):
                            resultContent = resultContent + '\t' + colsList[i] + ":" + user[i].__str__()
                        print(resultContent)

                    print("是否将结果进行保存？输入s进行保存")


                else:
                    print("您所查询的年级下暂时不存在已注册的学生，请确认您的输入")
            else:
                print("您所查询的年级不存在，请确认您的输入")
        else:
            print("您所查询的学校不存在，请确认您的输入是否正确")





# 输出指定姓名（nickname）的所有用户信息，如果有重复，就把所有的输出来
def findAllStudentByNickname(attributes,nickname, cursor):
    sql = "SELECT %s FROM yzbc.yz_user where nickname = '%s'" % (attributes, nickname)
    cursor.execute(sql)
    result = cursor.fetchone()
    cols = cursor.description
    if result:
        print("当前账号的信息如下：")
        colsList = []
        resultContent = ""
        for col in cols:
            colsList.append(col[0])
        for i in range(colsList.__len__()):
            resultContent = resultContent + '\t' + colsList[i] + ":" + result[i].__str__()
        print(resultContent)

    else:
        print("找不到对应的账号信息")




# 查找一个班级所有学生的账号
def findAllStudentByClass(attributes,className, cursor):
    nameList = className.split('-')
    if nameList.__len__() !=  3:
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
                sql = "SELECT id FROM yzbc.yz_jxgl_class where gradeid = %s and schoolid = %s and classname='%s'" % (
                gradeId, schoolId, className)
                cursor.execute(sql)
                classData = cursor.fetchall()
                if classData:
                    classId = classData[0]
                    sql = "SELECT uid FROM yzbc.yz_jxgl_student where classid = %s" % (classId)
                    cursor.execute(sql)
                    stuData = cursor.fetchall()
                    if stuData:
                        result = []
                        cols = []
                        for stu in stuData:
                            uid = stu[0]
                            sql = "SELECT %s FROM yzbc.yz_user where id = %s" % (attributes,uid)
                            cursor.execute(sql)
                            userData = cursor.fetchone()
                            cols = cursor.description
                            result.append(userData)
                        print("%s的所有学生账号详细情况如下：" % className)
                        colsList = []
                        for col in cols:
                            colsList.append(col[0])
                        for user in result:
                            resultContent = ""
                            for i in range(colsList.__len__()):
                                resultContent = resultContent + '\t' + colsList[i] + ":" + user[i].__str__()
                            print(resultContent)

                        print("是否将结果进行保存？输入s进行保存")
                        saveornot = input().strip()
                        # 进行文件的保存；在当前文件夹下进行文件的存放
                        if saveornot == 's':

                            # path = "\%s\%s" %(schoolName,gradeName)
                            path = '/' + schoolName
                            os.mkdir(path)
                            os.chdir(path)
                            # path = '/' + gradeName
                            # os.mkdir(path)
                            # os.chdir(path)
                            #
                            # with open("data.csv", "w+", newline="") as datacsv:
                            #     # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
                            #     csvwriter = csv.writer(datacsv, dialect=("csv"))
                            #     # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
                            #     csvwriter.writerow(cols)
                            #     for item in result:
                            #         csvwriter.writerow(item)





                    else:
                        print("您所查询的班级下暂时不存在已注册的学生，请确认您的输入")
                else:
                    print("您所查询的班级不存在，请确认您的输入")
            else:
                print("您所查询的年级不存在，请确认您的输入")
        else:
            print("您所查询的学校不存在，请确认您的输入是否正确")



# 输出一个学校的所有账号
def findStudentBySchool(attributes, schoolname, cursor):
    sql = "SELECT id FROM yzbc.yz_jxgl_school where schoolname  = '%s'" %schoolname
    cursor.execute(sql)
    schoolId = cursor.fetchone()
    if schoolId:
        sql = "SELECT uid FROM yzbc.yz_jxgl_student where schoolid = %s" %schoolId[0]
        cursor.execute(sql)
        uid = cursor.fetchall()
        inforOfAll = []
        cols = ()
        # 对每一个uid在user表中进行检索
        for uid in uid:
            sql = "SELECT %s FROM yzbc.yz_user where id = %s" % (attributes, uid[0])
            cursor.execute(sql)
            inforOfUser = cursor.fetchone()
            cols = cursor.description
            inforOfAll.append(inforOfUser)
        print("%s的所有学生账号详细情况如下：" %schoolname)
        colsList = []
        for col in cols:
            colsList.append(col[0])
        for user in inforOfAll:
            resultContent = ""
            for i in range(colsList.__len__()):
                resultContent = resultContent + '\t' + colsList[i] + ":" + user[i].__str__()
            print(resultContent)

    else:
        print("您所查询的学校不存在")

# 输出一个地区的所有学校
def findSchoolByProvince(attributes,place, cursor):
    sql = "SELECT %s FROM yzbc.yz_jxgl_school where province like '%%%%%s%%%%' or city like '%%%%%s%%%%'" % \
          (attributes, place, place)
    cursor.execute(sql)
    result = cursor.fetchall()
    cols = cursor.description
    if result:
        print("%s地区的学校信息如下：" % place)
        colsList = []
        resultContent = ""
        for col in cols:
            colsList.append(col[0])
        for i in range(colsList.__len__()):
            resultContent = resultContent + '\t' + colsList[i] + ":" + result[i].__str__()
        print(resultContent)
    else:
        print("%s地区没有学校正在使用本产品" % place)


# 查询某个学生的具体信息（必须包含账号和密码）
# ls username = 3180702009
def findStudentById(attributes,username, cursor):
    sql = "SELECT %s FROM yzbc.yz_user where username = '%s'" % (attributes, username)
    cursor.execute(sql)
    result = cursor.fetchone()
    cols = cursor.description
    if result:
        print("当前账号的信息如下：")
        colsList = []
        resultContent = ""
        for col in cols:
            colsList.append(col[0])
        for i in range(colsList.__len__()):
            resultContent = resultContent + '\t' + colsList[i] + ":" + result[i].__str__()
        print(resultContent)
    else:
        print("找不到对应的账号信息")

# def ls_main(cursor, des):
#     des = des.strip()
#     desList = des.split(' ')
#     desFinList = []
#     for item in desList:
#         if '=' in item:
#             temp = item.split('=')
#             desFinList.append(temp)
#         else:
#             desFinList.append(item)
#     if desFinList.__len__()>2:
#         print("您的输入有误，请按照要求进行输入")
#         return
#     else:
#         attributes = desFinList[0]
#         condition = desFinList[1]
#         # 按照账号名查找学生的账号，密码以及其他信息
#         if condition[0] == "username":
#             findStudentById(attributes, condition[1], cursor)
#         # 按照学校名称查找这个学校所有账号信息
#         elif condition[0] == "schoolname":
#             findStudentBySchool(attributes, condition[1], cursor)
#         # 查找一个班级的所有学生账号
#         elif condition[0] == "class":
#             findAllStudentByClass(attributes, condition[1], cursor)
#         # 按照地区名称，查找所有学校
#         elif condition[0] == "place":
#             findSchoolByProvince(attributes, condition[1], cursor)
#         elif condition[0] == "name":
#             findAllStudentByNickname(attributes, condition[1], cursor)
#         else:
#             print("暂时未提供此服务，或者用户输入错误，请按照说明进行系统使用，可以输入help以查看帮助")


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
    des = sys.argv
    desList = des
    desFinList = []
    for item in desList:
        if '=' in item:
            temp = item.split('=')
            desFinList.append(temp)
        else:
            desFinList.append(item)
    if desFinList.__len__() > 3:
        print("您的输入有误，请按照要求进行输入")
    else:
        attributes = desFinList[1]
        condition = desFinList[2]
        # 按照账号名查找学生的账号，密码以及其他信息
        if condition[0] == "username":
            findStudentById(attributes, condition[1], cursor)
        # 按照学校名称查找这个学校所有账号信息
        elif condition[0] == "schoolname":
            findStudentBySchool(attributes, condition[1], cursor)
        elif condition[0] == "grade":
            findAllStudentByGradeName(attributes, condition[1], cursor)
        # 查找一个班级的所有学生账号
        elif condition[0] == "class":
            findAllStudentByClass(attributes, condition[1], cursor)
        # 按照地区名称，查找所有学校
        elif condition[0] == "place":
            findSchoolByProvince(attributes, condition[1], cursor)
        elif condition[0] == "name":
            findAllStudentByNickname(attributes, condition[1], cursor)
        else:
            print("暂时未提供此服务，或者用户输入错误，请按照说明进行系统使用，可以输入help以查看帮助")
