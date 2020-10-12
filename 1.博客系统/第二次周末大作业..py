# 作业：用代码模拟博客园系统
# 项目分析：
# 一．首先程序启动，页面显示下面内容供用户选择：
# 1.请登录
# 2.请注册
# 3.进入文章页面
# 4.进入评论页面
# 5.进入日记页面
# 6.进入收藏页面
# 7.注销账号
# 8.退出整个程序
#
# 二．必须实现的功能：
# 1.注册功能要求：
# a.用户名、密码要记录在文件中。
# b.用户名要求：只能含有字母或者数字不能含有特殊字符并且确保用户名唯一。
# c.密码要求：长度要在6~14个字符之间。
#
# 2.登录功能要求：
# a.用户输入用户名、密码进行登录验证。
# b.登录成功之后，才可以访问3~7选项，如果没有登录或者登录不成功时访问3~7选项，不允许访问，让其先登录。
# c.超过三次登录还未成功，则退出整个程序。
#
# 3.进入文章页面要求：
# a.提示欢迎xx进入文章页面。
# b.此时用户可以选择：直接写入内容，还是导入md文件。
#
# ①如果选择直接写内容：让学生直接写文件名|文件内容......最后创建一个文章。
# input ---->  自定义模块| fkjdshfkladshfskldafhjaksdfdsjk
# split
# 文件名: 自定义模块
# 文件内容: fkjdshfkladshfskldafhjaksdfdsjk
# 创建文件:
# ②如果选择导入md文件：让用户输入已经准备好的md文件的文件路径（相对路径即可：比如函数的进阶.md），
# 然后将此md文件的全部内容写入文章（函数的进阶.text）中。
#
# 4.进入评论页面要求：
# 提示欢迎xx进入评论页面。
#
# 5.进入日记页面要求：
# 提示欢迎xx进入日记页面。
#
# 6.进入收藏页面要求：
# 提示欢迎xx进入收藏页面。
#
# 7.注销账号要求：
# 不是退出整个程序，而是将已经登录的状态变成未登录状态（访问3~7选项时需要重新登录）。
#
# 8.退出整个程序要求：
# 就是结束整个程序。
#
# 三．选做功能：
# 评论页面要求：
# a.提示欢迎xx进入评论页面。
# b.让用户选择要评论的文章。
# 这个需要借助于os模块实现此功能，将所有的文章文件单独放置在一个目录(文件夹)中。
# 利用os模块listdir功能,可以将一个目录下所有的文件名以字符串的形式存在一个列表中并返回。
# c.选择要评论的文章之后，先要将原文章内容全部读一遍，然后输入的你的评论，
# 评论要过滤掉这些敏感字符："苍老师", "东京热", "武藤兰", "波多野结衣"，替换成等长度的"*"之后，写在文章的评论区最下面。
# 文章的结构：
#
# 文章具体内容
# .......
#
# 评论区：
# -----------------------------------------
#           (用户名)xx:
#           评论内容
#           (用户名)oo:
#           评论内容
# 原文章最下面如果没有以下两行：
# """
# 评论区：
# -----------------------------------------
# """
# 就加上这两行在写入评论，如果有这两行则直接在下面顺延写上：
# 	(用户名)xx:
#           	评论内容
import sys
import os

web_cookie = {
    'username': None,
    'flag': False
}


def bad_delete(s):
    li = ['苍老师', '东京热', '武藤兰', '波多野结衣']
    for i in li:
        if i in s:
            s = s.replace(i, len(i) * '*')
            bad_delete(s)
    return s


def wrapper(f):
    def inner(*args, **kwargs):
        if web_cookie['flag']:
            f(*args, **kwargs)
        else:
            print('请先登录!')
            login()
    return inner


def login():
    user_info = {}
    count = 0
    with open('users', encoding='utf-8', mode='r') as f:
        for line in f:
            user_info[line.split('|')[0].strip()] = line.split('|')[1].strip()
    while True:
        if web_cookie['flag']:
            print('不要重复登录!')
            break
        username = input('请输入登录用户名: ').strip()
        password = input('请输入登录密码: ').strip()
        if username in user_info and user_info[username] == password:
            web_cookie['flag'] = True
            web_cookie['username'] = username
            print('登录成功!')
            break
        else:
            if count == 2:
                print('尝试次数过多,程序退出!')
                quit_all()
            print('登录失败!')
            count += 1


def register():
    user_list = []
    with open('users', encoding='utf-8', mode='r+') as f:
        user = input('请输入注册用户名: ').strip()
        for line in f:
            user_list.append(line.split('|')[0])
        if user.isalnum() and user not in user_list:
            password = input('请输入注册密码: ').strip()
            if len(password) > 5:
                f.write(f'{user}|{password}\n')
                print('注册成功!')
            else:
                print('密码长度必须大于等于6位,请重新输入!')
                register()
        else:
            print('用户名不符合规则或已存在,请重新注册!')
            register()


@wrapper
def article():
    comment_title = '''

评论区：
-----------------------------------------
'''
    print(f'欢迎{web_cookie["username"]}进入文章页面')
    print('''
        1.直接写入内容
        2.导入md文件
    ''')
    c = input('请选择 1 or 2 >>> ')
    if c == '1':
        content = input('请输入文件名|内容: ')
        with open('文章/' + content.split('|')[0].strip(), encoding='utf-8', mode='w') as f:
            f.write(content.split('|')[1].strip())
            f.write(comment_title)
    else:
        p1 = input('请输入md文件路径: ')
        p2 = p1.replace('md', 'txt')
        with open(p1, encoding='utf-8') as f1, open('文章/' + p2, encoding='utf-8', mode='w') as f2:
            for line in f1:
                f2.write(line)
            f2.write(comment_title)


@wrapper
def comment():
    print(f'欢迎{web_cookie["username"]}进入评论页面')
    article_list = os.listdir('文章')
    print(list(enumerate(article_list)))
    c = input('请输入要评论文章的序号: ')
    content1 = input('请输入评论: ')
    content2 = f'{web_cookie["username"]}:\n{bad_delete(content1)}\n'
    with open('文章/' + article_list[int(c)], encoding='utf-8', mode='a') as f:
        f.write(content2)


@wrapper
def diary():
    print(f'欢迎{web_cookie["username"]}进入日记页面')


@wrapper
def collection():
    print(f'欢迎{web_cookie["username"]}进入收藏页面')


@wrapper
def logoff():
    web_cookie['username'] = None
    web_cookie['flag'] = False
    print('注销成功!')


def quit_all():
    sys.exit(0)


select_func = {
    '1': login,
    '2': register,
    '3': article,
    '4': comment,
    '5': diary,
    '6': collection,
    '7': logoff,
    '8': quit_all
}

while True:
    print('''
        1.登录
        2.注册
        3.文章页面
        4.评论页面
        5.日记页面
        6.收藏页面
        7.注销
        8.退出
        ''')
    c = input('请输入功能序号: ').strip()
    if c in map(str, range(1, 9)):
        select_func[c]()
    else:
        print('输入错误,请重试!')
