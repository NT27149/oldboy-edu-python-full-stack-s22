# 文件a1.txt内容(选做题)
# 序号 部门 人数 平均年龄 备注
#
# 1 python 30 26 单身狗
#
# 2 Linux 26 30 没对象
#
# 3 运营部 20 24 女生多
#
# .......
#
# 通过代码，将其构建成这种数据类型：
#
# [{'序号':'1','部门':Python,'人数':30,'平均年龄':26,'备注':'单身狗'},
#
# ......]

l1 = []
with open('a1.txt',mode='r') as f :
    title = f.readline().strip().split()
    for i in f:
        lis = i.split()
        dic1 = {}
        for em in range(len(lis)):
            if lis[em].isdecimal():
                dic1[title[em]] = int(lis[em])
            else:
                dic1[title[em]] = lis[em]
        l1.append(dic1)
print(l1)