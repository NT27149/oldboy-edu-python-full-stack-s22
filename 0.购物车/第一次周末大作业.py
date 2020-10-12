# 1.完成一个商城购物车的程序。
# 商品信息在文件存储的，存储形式：
# name price
# 电脑 1999
# 鼠标 10
# 游艇 20
# 美女 998
# .......
#
# 要求:
# 1，用户先给自己的账户充钱：比如先充3000元。
# 2，读取商品信息文件将文件中的数据转化成下面的格式：
# goods = [{"name": "电脑", "price": 1999},
# {"name": "鼠标", "price": 10},
# {"name": "游艇", "price": 20},
# {"name": "美女", "price": 998},
# ...... ]

# 2.页面显示 序号 + 商品名称 + 商品价格，如：
# 1 电脑 1999
# 2 鼠标 10
# …
# n 购物车结算
# q或者Q退出程序。

# 3.用户输入选择的商品序号，然后打印商品名称及商品价格,并将此商品，添加到购物车，用户还可继续添加商品。
# 4.如果用户输入的商品序号有误，则提示输入有误，并重新输入。
# 5.用户输入n为购物车结算，依次显示用户购物车里面的商品，数量及单价，若充值的钱数不足，则让用户删除某商品，直至可以购买，若充值的钱数充足，则可以直接购买。
# 6.用户输入Q或者q退出程序。
# 7.退出程序之后，依次显示用户购买的商品，数量，单价，以及此次共消费多少钱，账户余额多少，并将购买信息写入文件。

money = 0
total_price = 0
dic = {}
goods = []
shopping_cart = {}
flag = 0

while True:
    s = input('请选择：r.充值 b.浏览商品 n.购物车结算 数字.将该商品添加进购物车 q.退出  >>> ').strip()
    if s.upper() == 'R':
        m = input('请输入充值钱数: ').strip()
        money += int(m)
        print(f'您现在的余额是{money}元')
    elif s.upper() == 'B':
        items_file = open('items.txt', encoding='utf-8', mode='r')
        title_list = items_file.readline().split()
        for line in items_file:
            dic = dict(zip(title_list, line.split()))
            if dic not in goods:
                goods.append(dic)
        for i in range(len(goods)):
            print(str(i + 1) + ' ' + goods[i]['name'] + ' ' + goods[i]['price'])
    elif s.isdecimal() and int(s) in range(1, len(goods) + 1):
        print(f"您已将{goods[int(s) - 1]['name']}添加进购物车!商品价格为{goods[int(s) - 1]['price']}元.")
        if goods[int(s) - 1]['name'] not in shopping_cart:
            shopping_cart[goods[int(s) - 1]['name']] = [int(goods[int(s) - 1]['price']), 1]
        else:
            shopping_cart[goods[int(s) - 1]['name']][1] += 1
    elif s.upper() == 'N':
        total_price = 0
        print('商品名称\t\t商品价格\t\t购买数量')
        for k, v in shopping_cart.items():
            print(k + '\t\t' + str(v[0]) + '\t\t' + str(v[1]))
            total_price += v[0] * v[1]
        if total_price > money:
            flag = 0
            print(f'您的余额不够,请删除商品!(总价{total_price},余额{money})')
            c = input('请输入要删除的物品名称  >>> ').strip()
            if c in shopping_cart:
                total_price -= shopping_cart[c][0] * shopping_cart[c][1]
                shopping_cart.pop(c)
            else:
                print('没有此商品,请重新输入!')
        else:
            print('可以购买!')
            money -= total_price
            flag = 1
    elif s.upper() == 'Q':
        if flag:
            shopping_file = open('shopping.txt', encoding='utf-8', mode='w')
            print('商品名称\t\t商品价格\t\t购买数量')
            for k, v in shopping_cart.items():
                s = k + '\t\t' + str(v[0]) + '\t\t' + str(v[1])
                print(s)
                shopping_file.write(s + '\n')
            print(f'此次消费共{total_price}元,余额还剩{money}元')
            shopping_file.write(f'此次消费共{total_price}元,余额还剩{money}元')
            shopping_file.close()
        else:
            print('您没有买任何商品!')
        break
    else:
        print('输入错误,请重试!')
