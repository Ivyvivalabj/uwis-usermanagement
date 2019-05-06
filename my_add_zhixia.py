# -*- coding:utf-8 -*-
import os as os
import csv
import hashlib
import time
import socket

import os as os
import csv
import hashlib
import time
import socket


# 查询本机ip地址:return: ip
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# 更新教师权限和负责的班级id
def updateTeacher(teachername,classids,quanxian,cursor, db):


    sql = "SELECT uid FROM yzbc.yz_jxgl_teacher where teachername = '%s' " % teachername
    cursor.execute(sql)
    teacherData = cursor.fetchone()
    if teacherData == None:
        if logG:
            print("找不到老师：%s" %teachername)
        return False
    else:
        uid = teacherData[0]
    sql = "SELECT quanxian FROM yzbc.yz_user where id = %s " % uid
    cursor.execute(sql)
    quanxianBefore = cursor.fetchone()[0]
    quanxianAfter = quanxianBefore + "," + quanxian
    sql = "UPDATE yzbc.yz_user SET quanxian = '%s' WHERE id = %s;"
    data = (quanxianAfter, uid)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        db.commit()
        if logG:
            print("教师用户数据更新已提交到数据库")
    except:
        if logG:
            print("教师用户数据写入发生错误")
        db.rollback()
        return False

    sql = "UPDATE yzbc.yz_jxgl_teacher SET classids = '%s' WHERE uid = %s;"
    data = (classids, uid)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        db.commit()
        if logG:
            print("教师数据更新已提交到数据库")
    except:
        if logG:
            print("教师数据写入发生错误")
        db.rollback()
        return False


# 先创建用户，再去创建学生
def creatStudent(row,schoolid,cursor, db,expire_date=94608000,password=123456):
    gradeName = row[0] + "级"
    className = row[1] + "班"
    # 根据学校id和年级名字可以唯一确定一个年级
    sql = "SELECT id FROM yzbc.yz_jxgl_grade where schoolid = %s and gradename = '%s'"
    data = (schoolid, gradeName)
    cursor.execute(sql % data)
    gradeData = cursor.fetchone()

    if gradeData == None:
        if logG:
            print("当前年级不存在")
        return False
    else:
        gradeId = gradeData[0]

    # 根据年级Id和班级名字可以唯一确定一个班级
    sql = "SELECT id,stugroupid FROM yzbc.yz_jxgl_class where gradeid = %s and classname = '%s'"
    data = (gradeId, className)
    cursor.execute(sql % data)

    classData = cursor.fetchone()
    if classData == None:
        if logG:
            print("当前班级不存在")
        return False
    else:
        classId = classData[0]
        stugroupId = classData[1]
    # 进行用户的创建
    username = row[3]
    password = hashlib.md5(b'123456').hexdigest()
    email = ''
    nickname = row[2]
    sex = ''
    regip = get_host_ip()
    regtime = time.time()
    groupid = stugroupId
    readlevel = 10
    quanxian = 'bbcode,login,lookuser,postreply,uploadfile,uploadhead,search,postread,lookread,download'
    jifen = 0
    tiandou = 0
    identification = ''
    sql = "INSERT INTO yzbc.yz_user(username, password,email, nickname,sex, regip,regtime,groupid, readlevel, quanxian" \
          ",jifen, tiandou, identification) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, '%s', %s, %s" \
          ", '%s');"
    data = (username, password, email, nickname, sex, regip, regtime, groupid, readlevel, quanxian, jifen, tiandou, identification)

    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        uid = cursor.lastrowid
        db.commit()
        print("学生用户数据已经提交到用户表中")
    except:
        if logG:
            print("学生用户数据写入发生错误")
        db.rollback()
        return False
    # 进行学生的创建
    uid = uid
    classid = classId
    gradeid = gradeId
    schoolid = schoolid
    expiredate = expire_date
    regtime = time.strftime("%Y%m%d", time.localtime())
    sql = "INSERT INTO yzbc.yz_jxgl_student(uid, classid,gradeid, schoolid,expiredate, regtime" \
          ") VALUES (%s, %s, %s, %s, %s, %s);"
    data = (uid, classid, gradeid, schoolid, expiredate, regtime)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        stuId = cursor.lastrowid
        db.commit()
        if logG:
            print("学生数据已经提交到用户表中")
        return uid
    except:
        if logG:
            print("学生数据写入发生错误")
        db.rollback()
        return False


# 根据学生学号检查学生是否已经在用户表中注册
def checkStudent(stuId,cursor):
    # 根据username去用户表中查找是否当前教师已经注册过
    sql = "SELECT id,nickname FROM yzbc.yz_user where username = '%s'"
    data = (stuId)
    cursor.execute(sql % data)
    result = cursor.fetchone()
    if result == None:
        if logG:
            print("当前用户不存在")
        return False
    else:
        return result


# 在班级表中创建班级
def createClass(classname,readsortid,studentgroupid,course,gradeid,schoolid,cursor,db,teacherids=0,expire_date=0):
    classname = classname
    sketch = ''
    readsortid = readsortid
    gradeid = gradeid
    courseids = course
    schoolid = schoolid
    stugroupid = studentgroupid
    expiredate = expire_date
    teacherids = teacherids
    creatdate = time.strftime("%Y%m%d", time.localtime())
    sql = "INSERT INTO yzbc.yz_jxgl_class(classname,sketch,readsortid, gradeid, courseids,schoolid,stugroupid,expiredate," \
          "teacherids,creatdate) VALUES ('%s', '%s',%s, %s,'%s', %s, %s,%s,%s,%s);"
    data = (classname, sketch, readsortid, gradeid, courseids, schoolid, stugroupid, expiredate, teacherids, creatdate)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        new_id = cursor.lastrowid
        db.commit()
        if logG:
            print("班级数据已经提交到数据库")
        return new_id
    except:
        if logG:
            print("班级数据写入发生错误")
        db.rollback()
        return False

    pass


# 通过班级板块Id查找班级id
def findClassByRSId(classRSId, cursor):
    # 根据username去用户表中查找是否当前教师已经注册过
    sql = "SELECT id FROM yzbc.yz_jxgl_class where readsortid = %s"
    data = (classRSId)
    cursor.execute(sql % data)
    result = cursor.fetchone()
    if result == None:
        if logG:
            print("当前年级不存在")
        return False
    else:
        return result[0]


# 在年级表中创建年级
def createGrade(gradename,readsortid,schoolid,cursor, db, expiredate=0):
    creatdate = time.time()
    # SQL 插入语句
    sql = "INSERT INTO yzbc.yz_jxgl_grade(gradename, readsortid, schoolid, creatdate,expiredate) VALUES ('%s', %s, %s, %s, %s);"
    data = (gradename, readsortid, schoolid, creatdate, expiredate)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        new_id = cursor.lastrowid
        db.commit()
        if logG:
            print("年级数据已经提交到数据库")
        return new_id
    except:
        if logG:
            print("年级数据写入发生错误")
        db.rollback()
        return False


# 通过年级板块id查询年级表中对应年级的Id
def findGradeIdByRSid(gradeRSid, cursor):
    # 根据username去用户表中查找是否当前教师已经注册过
    sql = "SELECT id FROM yzbc.yz_jxgl_grade where readsortid = %s"
    data = (gradeRSid)
    cursor.execute(sql % data)
    result = cursor.fetchone()
    if result == None:
        if logG:
            print("当前年级不存在")
        return False
    else:
        return result[0]


# 检查年级、班级板块是否存在
def checkReadsort(title, pid, cursor):
    # 根据username去用户表中查找是否当前教师已经注册过
    sql = "SELECT id FROM yzbc.yz_readsort where title = '%s' and pid = %s"
    data = (title, pid)
    cursor.execute(sql % data)
    result = cursor.fetchone()
    if result == None:
        if logG:
            print("当前板块不存在")
        return False
    else:
        return result[0]


# 更新板块权限
def updateReadsort(readsortId, usergroupId,cursor, db):
    # 根据给定的板块Id,查询当前板块的allowgroupids属性，并将给定的用户组，添加到allowgroupids后面，用逗号隔开
    sql = "SELECT allowgroupids FROM yzbc.yz_readsort where id  = %s" % readsortId
    cursor.execute(sql)
    allowgroupids = cursor.fetchone()[0]
    allowgroupids = allowgroupids + usergroupId.__str__() + ','
    # 将给定用户组id放入指定板块的allowgroupids中
    sql = "UPDATE yzbc.yz_readsort SET allowgroupids = '%s' WHERE id = %s;"
    data = (allowgroupids, readsortId)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        db.commit()
        if logG:
            print("用户组权限更新已提交到数据库")
    except:
        if logG:
            print("用户组权限更新写入发生错误")
        db.rollback()
        return False


# 创建用户组
def createUserGroup(usergroupname, cursor, db, quanxian=''):
    readlevel = 10
    quanxian ='bbcode,login,lookuser,uploadfile,uploadhead,search,postread,lookread,download,delread,editread,nopostreadcheck,nopostreplycheck,postreply,editreply,htmlcode' + quanxian
    # SQL 插入语句
    sql = "INSERT INTO yzbc.yz_usergroup(usergroupname, quanxian  , readlevel) VALUES ('%s', '%s', %s);"
    data = (usergroupname, quanxian, readlevel)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        new_id = cursor.lastrowid
        db.commit()
        if logG:
            print("用户组数据已经提交到数据库")
        return new_id
    except:
        if logG:
            print("用户组数据写入发生错误")
        db.rollback()
        return False


# 检查当前用户组是否存在
def checkUserGroup(usergroupName,cursor):
    # 根据username去用户表中查找是否当前教师已经注册过
    sql = "SELECT id FROM yzbc.yz_usergroup where usergroupname = '%s'" % usergroupName
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        if logG:
            print("当前用户组不存在用户组表中")
        return False
    else:
        return result[0]


# 创建老师
def createTeacher(name,phone,schoolid,cursor,db,quanxian='',expire_date=94608000,groupid=5,password=123456):
    username = 'js' + phone
    password = hashlib.md5(b'123456').hexdigest()
    email = ''
    nickname = name
    sex = ''
    regip = get_host_ip()
    phone = phone
    regtime = time.time()
    groupid = groupid
    readlevel = 10
    quanxian = 'bbcode,login,lookuser,postreply,uploadfile,uploadhead,search,postread,lookread,download,delread,editread' \
               ',nopostreadcheck, noverifycode, htmlcode, delreply, editreply, nopostreplycheck, nopostingtimeinterval,'+ quanxian
    jifen = 0
    tiandou = 0
    identification = expire_date

    # 首先需要在用户表中创建用户
    # SQL 插入语句
    sql = "INSERT INTO yzbc.yz_user(username, password,email, nickname,sex, regip, phone,regtime,groupid, readlevel, quanxian" \
          ",jifen, tiandou, identification) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, '%s', %s, %s" \
          ", '%s');"
    data = (username, password,email, nickname,sex, regip, phone,regtime,groupid, readlevel, quanxian,jifen, tiandou,
            identification)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        uid = cursor.lastrowid
        db.commit()
        if logG:
            print("教师用户数据已经提交到用户表中")
    except:
        if logG:
            print("教师用户数据写入发生错误")
        db.rollback()
        return False

    # 然后是在老师表中创建老师
    uid = uid
    teachername = name
    schoolid = schoolid
    expiredate = expire_date
    regtime = time.strftime("%Y%m%d", time.localtime())

    sql = "INSERT INTO  yzbc.yz_jxgl_teacher(uid, teachername,schoolid, expiredate,regtime) VALUES (%s, '%s', %s, %s, %s);"
    data = (uid, teachername, schoolid, expiredate, regtime)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        id = cursor.lastrowid
        db.commit()
        if logG:
            print("教师用户数据已经提交到教师表中")
        return id
    except:
        if logG:
            print("教师用户数据写入发生错误")
        db.rollback()
        return False


# 创建学校，在学校表中插入数据
def createSchool(schoolname, cursor, schoolRSid, province, city, db, stugroupid=0, expire_date=''):
    creatdate = time.strftime("%Y%m%d", time.localtime())
    sketch = ''
    readsortid = schoolRSid
    # SQL 插入语句
    sql = "INSERT INTO yzbc.yz_jxgl_school(schoolname,sketch,readsortid,stugroupid, province, city, creatdate) " \
          "VALUES ('%s', '%s',%s,%s, '%s', '%s',%s);"
    data = (schoolname, sketch, readsortid, stugroupid, province, city, creatdate)
    # try:
    # 执行sql语句
    cursor.execute(sql % data)
    # 提交到数据库执行
    new_id = cursor.lastrowid
    db.commit()
    if logG:
        print("学校数据已经提交到数据库")
    return new_id


# 通过学校的名字查询学校的ID
def findSchoolByName(schoolname,cursor):
    sql = "SELECT id FROM yzbc.yz_jxgl_school where schoolname  = '%s'" % schoolname
    cursor.execute(sql)
    id = cursor.fetchone()
    if id:
        return id[0]
    else:
        return False


# 检查当前的老师是否存在
def checkTeacher(phone, cursor):
    # 根据username去用户表中查找是否当前教师已经注册过
    username = 'js' + phone
    sql = "SELECT id FROM yzbc.yz_user where username = '%s'" % username
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        if logG:
            print("当前老师不存在用户表中")
        return False
    else:
        # 根据userId去老师表中查找是否已经在老师表中注册过
        sql = "SELECT id FROM yzbc.yz_jxgl_teacher where uid = %s" % result[0]
        cursor.execute(sql)
        teacherData = cursor.fetchone()
        if teacherData:
            teacherId = teacherData[0]
            return teacherId
        else:
            if logG:
                print("教师存在于用户表却不存在教师表中")
            return False


# 创建板块函数  所需参数:$pid:父板块id   $title:板块名$label：板块标签
def createReadsort(title, cursor,db, pid =0 , allowgroupids = '', label = ''):
    content = title
    allowgroupids = '5,' + allowgroupids + ','
    # SQL 插入语句
    sql = "INSERT INTO yzbc.yz_readsort(pid, title, content, label, allowgroupids) VALUES (%s, '%s', '%s', '%s', '%s');"
    data = (pid, title, content, label, allowgroupids)
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 提交到数据库执行
        new_id = cursor.lastrowid
        db.commit()
        if logG:
            print("板块数据已经提交到数据库")
        return new_id
    except:
        if logG:
            print("板块数据写入发生错误")
        db.rollback()
        return False


# 根据板块名检查板块是否存在；若存在，返回值为包含id和title的数组,若不存在，则返回false
def checkTitleExist(title, cursor):
    result = []
    result.append(title)
    sql = "SELECT id FROM yzbc.yz_readsort where title  = '%s'" % title
    cursor.execute(sql)
    id = cursor.fetchone()
    if id:
        result.append(id[0])
        return result
    else:
        return False


def zhixia_main(entry, path, db, cursor):
    # 文件是否齐全检查过程
    somethingWrong = False
    dirName1 = entry.name
    path2 = path + "\\" + dirName1
    with os.scandir(path2) as it3:
        for entry3 in it3:
            haveCSV = False
            haveGrade_class_teacher_course = False
            haveTeacher = False
            filenameList = []
            pathFinal = path2 + "\\" + entry3.name
            # 对校级目录下的文件是否齐全进行检查
            for filename in os.listdir(pathFinal):
                filenameList.append(filename)
            for name in filenameList:
                if name.endswith('csv'):
                    haveCSV = True
                if name[0:3] == "老师表":
                    haveTeacher = True
                if name[0:9] == "年级班级老师课程表":
                    haveGrade_class_teacher_course = True
            if haveGrade_class_teacher_course == False:
                somethingWrong = True
                if logG:
                    print("%s路径下年级班级老师课程表不存在" % pathFinal)
            if haveTeacher == False:
                somethingWrong = True
                if logG:
                    print("%s路径下老师课程表不存在" % pathFinal)
            if haveCSV == False:
                somethingWrong = True
                if logG:
                    print("%s路径下学生名单不存在" % pathFinal)
    if somethingWrong:
        exit(0)
    else:
        print("文件检查通过")
    print("--------------------------------------------")

    # 市级目录读取
    with os.scandir(path) as it2:
        for entry2 in it2:
            if not entry2.name.startswith('.') and entry2.is_dir() and entry2.name != "logs" and entry2 != None:
                dirName2 = entry2.name
                path3 = path + "\\" + dirName2
                if logG:
                    print("%s目录正在安装" % dirName2)
                cityRSid = 0
                whetherExistData = checkTitleExist(dirName2, cursor)
                # 当前读取的文件夹所对应的板块存在
                if whetherExistData:
                    cityRSid = whetherExistData[1]
                    if logG:
                        print("当前读取文件加所对应板块已经存在，板块id: %s" % cityRSid)
                # 当前读取的文件夹所对应的板块不存在
                else:
                    cityRSid = createReadsort(dirName2, cursor, db, pid=0, label=dirName2)
                    if cityRSid == False:
                        print("市级数据发生数据回滚，请用户检查数据")
                        exit(0)
                    else:
                        if logG:
                            print("创建市级板块成功，板块id:%s" % cityRSid)

                # 校级目录读取
                with os.scandir(path3) as it3:
                    for entry3 in it3:
                        dirName3 = entry3.name
                        path4 = path3 + "\\" + dirName3
                        if logG:
                            print("%s目录正在安装" % dirName3)
                        schoolRSid = 0
                        schoolId = 0
                        whetherExistData = checkTitleExist(dirName3, cursor)
                        # 当前读取的文件夹所对应的板块存在
                        if whetherExistData:
                            # 获取当前学校对应板块id
                            schoolRSid = whetherExistData[1]
                            if logG:
                                print("当前读取文件加所对应板块已经存在，板块id: %s" % schoolRSid)
                            schoolId = findSchoolByName(dirName3, cursor)
                            if logG:
                                print("当前读取文件加所对应学校已经存在，学校id: %s" % schoolId)


                        # 当前读取的文件夹所对应的板块不存在
                        else:
                            schoolRSid = createReadsort(dirName3, cursor, db, pid=cityRSid, label=dirName3)
                            schoolId = createSchool(dirName3, cursor, schoolRSid, dirName1, dirName2, db)
                            if schoolRSid == False or schoolId == False:
                                print("校级发生数据回滚，请用户检查数据")
                                exit(0)
                            else:
                                if logG:
                                    print("创建学校板块成功，板块id:%s" % schoolRSid)
                                    print("创建学校成功，学校id:%s" % schoolId)

                        # 对文件“校管表”、“老师表”中的内容，将老师的数据导入数据库
                        teacherTablePath = path4 + "\\" + "老师表.txt"
                        teacherFile = open(teacherTablePath, 'r', encoding='utf-8-sig')
                        teacherTable = teacherFile.readlines()
                        for teacher in teacherTable:
                            teacherInfor = teacher.split('，')
                            teacherId = checkTeacher(teacherInfor[1].strip(), cursor)
                            # 如果老师已经存在或者
                            if teacherId:
                                if logG:
                                    print("%s已经存在，不需要再创建" % teacherInfor[0])
                            # 如果老师不存在
                            else:
                                if logG:
                                    print("%s不存在，正在进行创建" % teacherInfor[0])
                                # name,phone,schoolid,cursor,db,quanxian='',expire_date=94608000,groupid=5,password=123456
                                teacherId = createTeacher(teacherInfor[0], teacherInfor[1], schoolId,
                                                          cursor, db)

                        # 对年级班级老师课程表中的数据进行处理
                        teacherCourseTablePath = path4 + "\\" + "年级班级老师课程表.txt"
                        teacherCourseTabelFile = open(teacherCourseTablePath, 'r', encoding='utf-8-sig')
                        teacherCourseTable = teacherCourseTabelFile.readlines()
                        # 进行老师权限的设置所需要用的字典
                        teacherQXTabel = {}
                        teacherClassId = {}
                        isgradenew = True

                        grade1 = []

                        for line in teacherCourseTable:
                            lineList = line.split('，')
                            gradeName = lineList[0].strip().__str__()

                            className = lineList[1].strip().__str__()

                            teacherName = lineList[2].strip().__str__()

                            courseName = lineList[3].strip().__str__()

                            usergroupName = dirName3 + gradeName + className
                            usergroupId = checkUserGroup(usergroupName, cursor)
                            # 用户组已经存在的情况
                            if usergroupId:
                                stugroupId = usergroupId
                                if logG:
                                    print("用户组已经存在，不需要更新")
                            # 用户组不存在的情况
                            else:
                                stugroupId = createUserGroup(usergroupName, cursor, db)
                                # updateReadsort(provinceRSid, stugroupId, cursor, db)
                                # print("更新省板块成功")
                                updateReadsort(cityRSid, stugroupId, cursor, db)
                                if logG:
                                    print("更新市板块成功")
                                updateReadsort(schoolRSid, stugroupId, cursor, db)
                                if logG:
                                    print("更新学校板块成功")

                            # 检查当前的年级板块是否存在,如果存在获取当前年级板块的Id
                            gradeRSid = checkReadsort(gradeName.__str__(), schoolRSid, cursor)

                            # 当前的年级板块存在的情况
                            if gradeRSid:
                                isgradenew = False
                                # 更新年级板块和对应用户组的权限
                                updateReadsort(gradeRSid, stugroupId, cursor, db)
                                if logG:
                                    print("更新年级板块成功")
                                gradeId = findGradeIdByRSid(gradeRSid, cursor)
                            # 当前的年级板块不存在的情况
                            else:
                                label = dirName3 + ',' + gradeName
                                gradeRSid = createReadsort(gradeName, cursor, db, pid=schoolRSid,
                                                           allowgroupids=stugroupId.__str__(), label=label)
                                if logG:
                                    print("创建年级板块成功，年级板块id: %s" % gradeRSid)
                                updateReadsort(gradeRSid, stugroupId, cursor, db)
                                if logG:
                                    print("更新年级板块成功")
                                gradeId = createGrade(gradeName, gradeRSid, schoolId, cursor, db)
                                if logG:
                                    print("创建年级成功，年级id: %s" % gradeId)

                            # 检查当前的班级板块是否存在，如果存在获取当前班级板块的Id
                            classRSid = checkReadsort(className, gradeRSid, cursor)
                            # 当前班级板块已经存在的情况
                            if classRSid:
                                classId = findClassByRSId(classRSid, cursor)
                                updateReadsort(classRSid, stugroupId, cursor, db)
                                if logG:
                                    print("%s班级板块已经存在，不需要再创建" % className)
                            # 当前班级板块不存在的情况
                            else:
                                label = dirName3 + ',' + gradeName + ',' + className + ',' + usergroupName
                                # 创建班级板块
                                classRSid = createReadsort(className, cursor, db, pid=gradeRSid,
                                                           allowgroupids=stugroupId.__str__(), label=label)
                                if logG:
                                    print("创建%s班级板块成功" % className)
                                updateReadsort(classRSid, stugroupId, cursor, db)
                                if logG:
                                    print("更新%s板块成功" % className)

                                # 创建班级
                                classId = createClass(className, classRSid, stugroupId, courseName, gradeId,
                                                      schoolId, cursor, db)
                                if logG:
                                    print("创建%s成功" % className)

                                # 获取对应年级的标准化课件

                                # 首先去找是否有对应课程编号的板块
                                sql = "SELECT id FROM yzbc.yz_readsort where title like '%%%%%s%%%%' " % courseName
                                cursor.execute(sql)
                                courseReadSortId = cursor.fetchone()
                                if courseReadSortId == None:
                                    if logG:
                                        print("未找到当前年级所对应的课程板块")
                                else:
                                    # 如果当前找到的课程板块不为空
                                    # 获取当前板块下的所有帖子
                                    sql = "SELECT title,content FROM yzbc.yz_read where sortid  = %s " % \
                                          courseReadSortId[0]
                                    cursor.execute(sql)
                                    courseRead = cursor.fetchall()
                                    for read in courseRead:
                                        needContent = read[1]
                                        needTitle = read[0]
                                        uid = 1
                                        sortId = classRSid
                                        sql = "INSERT INTO yzbc.yz_read(uid, sortid, title, content) VALUES (%s, %s, '%s', '%s');"
                                        data = (uid, sortId, needTitle, needContent)
                                        try:
                                            # 执行sql语句
                                            cursor.execute(sql % data)
                                            # 提交到数据库执行
                                            db.commit()
                                            if logG:
                                                print("%s帖子数据已经提交到数据库" % needTitle)
                                        except:
                                            if logG:
                                                print("帖子数据写入发生错误，进行数据回滚")
                                            db.rollback()

                            # 如果在字典中存在老师的名字，则说明这位老师负责不止一个班级
                            if teacherName in teacherQXTabel:
                                # 为老师添加班级
                                teacherClassId[teacherName] = teacherClassId[
                                                                  teacherName] + "," + classId.__str__()
                                # 如果年级板块是新建的，则说明，这位老师负责的不同班级在不同年级
                                if isgradenew:
                                    teacherQXTabel[teacherName] = teacherQXTabel[
                                                                      teacherName] + "," + gradeRSid.__str__() + "," + classRSid.__str__()
                                # 如果年级板块不是新建的，则说明，这位老师负责的不同班级在同一年级，在权限设置时，就不再需要添加年级板块的权限
                                else:
                                    teacherQXTabel[teacherName] = teacherQXTabel[
                                                                      teacherName] + "," + classRSid.__str__()




                            # 如果在字典中不存在老师的名字，则说明是第一次进行当前老师负责班级数据录入
                            else:
                                # 为老师添加班级
                                teacherClassId[teacherName] = classId.__str__()
                                # 为老师添加权限
                                teacherQXTabel[
                                    teacherName] = cityRSid.__str__() + ',' + schoolRSid.__str__() + ',' + gradeRSid.__str__() + ',' + classRSid.__str__()

                        # 进行教师用户权限的更新
                        for key in teacherQXTabel:
                            updateTeacher(key, teacherClassId[key], teacherQXTabel[key], cursor, db)
                            if logG:
                                print("更新教师成功")

                        # 进行标准课件的更新
                        for line in teacherCourseTable:
                            lineList = line.split('，')
                            # 首先要找到班级板块
                            gradeRSid = checkReadsort(gradeName.__str__(), schoolRSid, cursor)
                            classRSid = checkReadsort(className, gradeRSid, cursor)
                            if gradeRSid & classRSid:
                                courseName = lineList[3].strip().__str__()
                                sql = "SELECT id FROM yzbc.yz_readsort where title like '%%%%%s%%%%' " % courseName
                                cursor.execute(sql)
                                # 找到标准课程所对应的板块ID
                                courseReadSortId = cursor.fetchone()
                                if courseReadSortId == None:
                                    if logG:
                                        print("当前年级板块没有标准课程，无需更新")
                                else:
                                    # 如果当前找到的课程板块不为空
                                    # 获取当前板块下的所有帖子
                                    sql = "SELECT title,content FROM yzbc.yz_read where sortid  = %s " % \
                                          courseReadSortId[0]
                                    cursor.execute(sql)
                                    courseRead = cursor.fetchall()
                                    # 对每一个标准课件的内容和当前班级下的标准课件的内容进行比较和替换
                                    for read in courseRead:
                                        # 标准课件的内容
                                        newContent = read[1]
                                        # 标准课件的标题
                                        newTitle = read[0]
                                        # 标准课件的uid
                                        uid = 1
                                        # 当前班级的板块id
                                        sortId = classRSid
                                        # 根据班级板块的id和帖子的标题进行在班级板块下的标准课件检查
                                        sql = "SELECT content,id FROM yzbc.yz_read where sortid  = %s and title = '%s' " % (sortId, newTitle)
                                        cursor.execute(sql)
                                        classRead = cursor.fetchall()
                                        if classRead:
                                            # 存在从标准课件中复制过来的课件；将标准课件中帖子的内容复制过来
                                            classReadId = classRead[1]
                                            classReadContent = classRead[0]
                                            sql = "UPDATE yzbc.yz_read SET content = '%s' WHERE id = %s;"
                                            data = (classReadContent, classReadId)
                                            try:
                                                # 执行sql语句
                                                cursor.execute(sql % data)
                                                # 提交到数据库执行
                                                db.commit()
                                                if logG:
                                                    print("标准课件已经更新")
                                            except:
                                                if logG:
                                                    print("标准课件数据写入发生错误，进行数据回滚")
                                                db.rollback()
                                                return False

                                        # 这篇帖子可能是后面加上去的
                                        else:
                                            # 那么直接把这篇帖子插入就可以了
                                            sql = "INSERT INTO yzbc.yz_read(uid, sortid, title, content) VALUES (%s, %s, '%s', '%s');"
                                            data = (uid, sortId, newTitle, newContent)
                                            print(sql % data)
                                            try:
                                                # 执行sql语句
                                                cursor.execute(sql % data)
                                                # 提交到数据库执行
                                                db.commit()
                                                if logG:
                                                    print("%s帖子数据已经提交到数据库" % needTitle)
                                            except:
                                                if logG:
                                                    print("帖子数据写入发生错误，进行数据回滚")
                                                db.rollback()
                            else:
                                if logG:
                                    print("班级或年级板块没有创建，不需要更新课程")

                        # 进行学生表数据的录入
                        with os.scandir(path4) as it4:
                            for entry4 in it4:
                                if entry4.name.endswith('.csv'):
                                    stuCSVPath = path4 + "\\" + entry4.name
                                    with open(stuCSVPath, newline='') as f:
                                        reader = csv.reader(f)
                                        for row in reader:
                                            if row == None: continue
                                            gradeName2 = row[0]
                                            className2 = row[1]
                                            stuName = row[2]
                                            stuId = row[3]
                                            # checkStudent 返回学生用户的id和学生用户的nickname
                                            whetherStuExist = checkStudent(stuId, cursor)
                                            # 如果学生存在
                                            if whetherStuExist:
                                                if whetherStuExist[1] != stuName:
                                                    # 将给定用户组id放入指定板块的allowgroupids中
                                                    sql = "UPDATE  yzbc.yz_user SET nickname = '%s' WHERE username = '%s';"
                                                    data = (stuName, stuId)
                                                    try:
                                                        # 执行sql语句
                                                        cursor.execute(sql % data)
                                                        # 提交到数据库执行
                                                        db.commit()
                                                        if logG:
                                                            print("用户昵称更新已提交到数据库")
                                                    except:
                                                        if logG:
                                                            print("写入发生错误，进行数据回滚")
                                                        db.rollback()
                                            # 如果用户不存在
                                            else:
                                                # 创建用户
                                                newStuId = creatStudent(row, schoolId, cursor, db)
                                                if newStuId:
                                                    if logG:
                                                        print("创建学生成功")
                                                else:
                                                    if logG:
                                                        print("创建学生失败")