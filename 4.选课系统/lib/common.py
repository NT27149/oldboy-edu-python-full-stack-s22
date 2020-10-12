import hashlib
import pickle
import os


def md5_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def choose_func(obj, i):
    try:
        methods = obj.function_list[i]
        if hasattr(obj, methods):
            getattr(obj, methods)()
    except Exception:
        print('输入有误,程序退出!')
        exit(0)


def manager_choose():
    print('1.创建课程\n2.创建学生账号\n3.查看所有课程\n4.查看所有学生\n5.退出程序')
    choose = input('请输入功能序号: ').strip()
    return int(choose) - 1


def student_choose():
    print('1.查看所有课程\n2.选择课程\n3.查看所选课程\n4.退出程序')
    choose = input('请输入功能序号: ').strip()
    return int(choose) - 1


def show_stu_cou(dbpath, filepath):
    with open(os.path.join(dbpath, filepath), mode='rb') as f:
        while True:
            try:
                print(pickle.load(f))
            except Exception:
                break
