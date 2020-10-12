import socket
import struct
import json
import os
import hashlib
MY_FILE = os.path.join(os.path.dirname(__file__),'百度网盘')
apple_id_path = os.path.join(os.path.dirname(__file__),'data','apple_id')
def md5_file(path):
    ret = hashlib.md5()
    with open(path,"rb") as f1:
        while True:
            content= f1.read(1024)
            if content:
                ret.update(content)
            else:
                return ret.hexdigest()
def read_file(four_bytes):
    with open(apple_id_path,encoding='utf-8',mode='r') as f1:
        for i in f1:
            if i.encode('utf-8')==four_bytes:
                return True
        else:return False


server = socket.socket()

server.bind(('127.0.0.1',9999))

server.listen(5)

conn, addr = server.accept()
four_bytes = conn.recv(1024)
if read_file(four_bytes):#判断账号密码正确吗
    conn.send('登录成功\n选择1上传或者2下载'.encode('utf-8'))
    four_bytes = conn.recv(1024)#接收
    if four_bytes==b'1':
       conn.send('1'.encode('utf-8'))
       # 1. 接收固定长度的4个字节
       four_bytes = conn.recv(4)

       # 2. 利用struct反解
       head_len = struct.unpack('i', four_bytes)[0]

       # 3. 接收bytes类型的报头
       head_dic_json_bytes = conn.recv(head_len)

       # 4. 将bytes类型的报头转化成json
       head_dic_json = head_dic_json_bytes.decode('utf-8')

       # 5. 将json类型报头转化成字典形式的报头
       head_dic = json.loads(head_dic_json)

       # 6. 接收原始数据
       with open(os.path.join(MY_FILE, head_dic['new_file_name']), mode='wb') as f1:

           total_size = 0

           while total_size < head_dic['file_size']:
               every_data = conn.recv(1024)
               f1.write(every_data)
               total_size += len(every_data)

    elif four_bytes==b'2':
        conn.send('2'.encode('utf-8'))
        l1 = os.listdir(os.path.join(os.path.dirname(__file__), '百度网盘'))
        json_l1=json.dumps(l1)
        conn.send(json_l1.encode('utf-8'))
        xz=conn.recv(1024)
        xzm=xz.decode('utf-8')
        FILE_PATH=os.path.join(os.path.dirname(__file__),'百度网盘', xzm)
        #  1.制作字典形式的报头
        head_dic = {
            'MD5': 123244546656,  # 提前获取
            'file_name': os.path.basename(FILE_PATH),  # 文件路径
            'file_size': os.path.getsize(FILE_PATH),  # 文件大小
            'new_file_name': 'demo1.mp4',
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
        conn.send(four_bytes)

        # 7.发送报头
        conn.send(head_dic_json_bytes)

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
                conn.send(every_data)
                if s == head_dic['file_size']:
                    break

else:
    conn.send('登录失败'.encode('utf-8'))

conn.close()
server.close()

