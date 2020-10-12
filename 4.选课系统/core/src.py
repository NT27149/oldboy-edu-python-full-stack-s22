from lib.common import md5_password
from lib.common import choose_func
from lib.common import manager_choose
from lib.common import student_choose
from lib.common import show_stu_cou
from conf.setting import DB_PATH
from log.createlog import create_logging
import pickle
import os


class Student:
    function_list = ['show_courses', 'select_course', 'show_selected_course', 'exit']

    def __init__(self, name):
        self.name = name
        self.courses = []

    def show_courses(self):
        show_stu_cou(DB_PATH, 'Course')
        choose_func(self, student_choose())

    def select_course(self):
        s = input('请输入课程的名称: ').strip()
        self.courses.append(s)
        print(f'添加{s}课程成功!')
        with open(os.path.join(DB_PATH, 'Student'), mode='rb') as f1, \
                open(os.path.join(DB_PATH, 'Student.bak'), mode='wb') as f2:
            while True:
                try:
                    stu_obj = pickle.load(f1)
                    pickle.dump(self if stu_obj.name == self.name else stu_obj, f2)
                except Exception:
                    break
        os.remove(os.path.join(DB_PATH, 'Student'))
        os.rename(os.path.join(DB_PATH, 'Student.bak'), os.path.join(DB_PATH, 'Student'))
        choose_func(self, student_choose())

    def show_selected_course(self):
        print(self.courses)
        choose_func(self, student_choose())

    def __str__(self):
        return f'名称:{self.name}  课程:{self.courses}'

    def exit(self):
        exit(0)


class Manager:
    function_list = ['create_course', 'create_student', 'show_courses', 'show_students', 'exit']

    def __init__(self, name):
        self.name = name

    def create_course(self):
        course_name = input('请输入课程名称: ').strip()
        course_price = input('请输入课程费用: ').strip()
        course_period = input('请输入课程周期: ').strip()
        with open(os.path.join(DB_PATH, 'Course'), mode='ab') as f:
            course_obj = Course(course_name, course_price, course_period)
            pickle.dump(course_obj, f)
            f.flush()
            create_logging(__name__, f'创建课程{course_name}成功!')
            choose_func(self, manager_choose())

    def create_student(self):
        student_name = input('请输入要创建的学生用户名: ').strip()
        student_password = input('请输入用户密码: ').strip()
        student_password = md5_password(student_password)
        with open(os.path.join(DB_PATH, 'UserInfo'), encoding='utf-8', mode='a') as f1:
            f1.write(f'{student_name}|{student_password}|Student\n')
            f1.flush()
        with open(os.path.join(DB_PATH, 'Student'), mode='ab') as f2:
            stu_obj = Student(student_name)
            pickle.dump(stu_obj, f2)
            f2.flush()
        create_logging(__name__, f'创建学生{student_name}成功!')
        choose_func(self, manager_choose())

    def show_courses(self):
        show_stu_cou(DB_PATH, 'Course')
        choose_func(self, manager_choose())

    def show_students(self):
        show_stu_cou(DB_PATH, 'Student')
        choose_func(self, manager_choose())

    def exit(self):
        exit(0)


class Course:
    def __init__(self, name, price, period):
        self.name = name
        self.price = price
        self.period = period
        self.teacher = None

    def __str__(self):
        return f'名称:{self.name}  价格:{self.price}  周期:{self.period}'


def login():
    count = 0
    while count < 3:
        username = input('欢迎来到选课系统!\n请输入用户名: ').strip()
        password = input('请输入密码: ').strip()
        password = md5_password(password)
        with open(os.path.join(DB_PATH, 'UserInfo'), encoding='utf-8') as f1:
            for userinfo in f1:
                u, p, t = userinfo.strip().split('|')
                if u == username and p == password:
                    if t == 'Student':
                        with open(os.path.join(DB_PATH, 'Student'), mode='rb') as f:
                            while True:
                                try:
                                    stu_obj = pickle.load(f)
                                    if stu_obj.name == username:
                                        choose_func(stu_obj, student_choose())
                                except Exception:
                                    break
                    else:
                        choose_func(Manager(username), manager_choose())
            else:
                print('用户名密码错误!')
                count += 1


def run():
    login()
