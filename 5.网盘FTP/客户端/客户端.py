import socket
import os
import json
import struct
import hashlib

def md5_str(n):
    ret = hashlib.md5()
    ret.update(n.encode("utf-8"))
    return ret.hexdigest()

def md5_file(path):
    ret = hashlib.md5()
    with open(path,"rb") as f1:
        while True:
            content= f1.read(1024)
            if content:
                ret.update(content)
            else:
                return ret.hexdigest()
# print(md5_file(r'绝对路径'))


def logon():
    username=input('请输入账号')
    password=input('请输入密码')
    password=md5_str(password)
    return username+'|'+password

def socket_client():
    client = socket.socket()
    client.connect(('127.0.0.1',9999))
    #将账号密码传过去
    client.send(logon().encode('utf-8'))
    # 接收登录成功\n选择1上传或者2下载
    ret=client.recv(1024)
    xz=input(ret.decode('utf-8'))
    client.send(xz.encode('utf-8'))#用户选择后发过去
    ret1 = client.recv(1024)
    if ret1==b'1':
        l1=os.listdir(os.path.join(os.path.dirname(__file__),'用户资料'))
        for i in l1:
            print(i,end=''+', ' )
        print('\n以上是你的所有文件')
        wjm=input('请输入文件名  将为你上传你的的专属网盘')
        #  1.制作字典形式的报头
        FILE_PATH = os.path.join(os.path.dirname(__file__),'用户资料', wjm)  # 文件路径
        head_dic = {
            'MD5': md5_file(FILE_PATH),  # 提前获取
            'file_name':FILE_PATH ,  # 文件路径
            'file_size': os.path.getsize(FILE_PATH),  # 文件大小
            'new_file_name': wjm,
        }

        # 2. 获取json形式的报头
        head_dic_json = json.dumps(head_dic)

        # 3. 获取bytes形式的报头
        head_dic_json_bytes = head_dic_json.encode('utf-8')

        # 4. 获取bytes报头的总字节数
        head_len = len(head_dic_json_bytes)

        # 5. 将bytes报头的总字节数转化成固定4个字节
        four_bytes = struct.pack('i', head_len)

        # 6. 发送固定的4个字节
        client.send(four_bytes)

        # 7.发送报头
        client.send(head_dic_json_bytes)

        # 8. 发送总数据
        '''
        循环条件设定: 
            1. 根据总子节数: file_size: 493701, 每次循环1024个,
            2. 每次取数据不为空,即可.
        '''
        with open(FILE_PATH, mode='rb') as f1:
            # while 1:
            #     every_data = f1.read(1024)
            #     if every_data:
            #         client.send(every_data)
            #     else:
            #         break
            s = 0
            while 1:
                every_data = f1.read(1024)
                s += len(every_data)
                client.send(every_data)
                if s == head_dic['file_size']:
                    break
    elif ret1==b'2':

        json_l1 = client.recv(1024)
        l1=json.loads(json_l1)
        for i in l1:
            print(i,end=''+', ' )
        xz=input('\n以上是你的所有文件,请输入文件下载')
        client.send(xz.encode('utf-8'))

        MY_FILE=FILE_PATH = os.path.join(os.path.dirname(__file__),'用户资料',xz )  # 文件路径

        # 1. 接收固定长度的4个字节
        four_bytes = client.recv(4)

        # 2. 利用struct反解
        head_len = struct.unpack('i', four_bytes)[0]

        # 3. 接收bytes类型的报头
        head_dic_json_bytes = client.recv(head_len)

        # 4. 将bytes类型的报头转化成json
        head_dic_json = head_dic_json_bytes.decode('utf-8')

        # 5. 将json类型报头转化成字典形式的报头
        head_dic = json.loads(head_dic_json)

        # 有一个MD5校验

        # 6. 接收原始数据
        with open(MY_FILE, mode='wb') as f1:

            total_size = 0

            while total_size < head_dic['file_size']:
                every_data = client.recv(1024)
                f1.write(every_data)
                total_size += len(every_data)



    client.close()#关闭客户端
socket_client()#调用函数
    # ret1 = client.recv(1024)
    # if ret1==b'1':
    #     cxwjm = inp