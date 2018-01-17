# coding=utf-8

from collections import Counter


# 1、单数
def isDan(mychard):
    flag = False
    if len(mychard) == 1:
        flag = True
    return flag, mychard[0]


# 2、对子
def isDuiZi(mychard):
    flag = False
    if len(mychard) == 2:
        if (mychard[0] == mychard[1]):
            flag = True
    return flag, mychard[0]


# 3、三不带
def isSanBuDai(mychard):
    flag = False
    if len(mychard) == 3:
        if (mychard[0] == mychard[1]) and (mychard[1] == mychard[2]):
            flag = True
    return flag, mychard[0]


# 4、三带一
def isSanDaiYi(mychard):
    flag = False
    if len(mychard) == 4:
        if (isSanBuDai(mychard[0:3])[0] and mychard[2] != mychard[3]) is True:
            flag = True
            return flag, mychard[0]
        elif (isSanBuDai(mychard[1:4])[0] and mychard[0] != mychard[1]) is True:
            flag = True
            return flag, mychard[1]
    return flag, mychard[0]


# 三带对子
def isSanDaiDuiZi(mychard):
    flag = False
    print "isSanDaiDuiZi"
    print len(mychard)
    if len(mychard) == 5:
        if (isDuiZi(mychard[0:2])[0] and isSanBuDai(mychard[2:5])[0]) is True:
            flag = True
            return flag, mychard[2]
        elif (isDuiZi(mychard[3:5])[0] and isSanBuDai(mychard[0:3])[0]) is True:
            flag = True
            return flag, mychard[3]
    return flag, mychard[0]


# 5、炸弹
def isBoom(mychard):
    flag = False
    if len(mychard) == 4:
        if (mychard[0] == mychard[1]) and (mychard[1] == mychard[2]) and (mychard[2] == mychard[3]):
            flag = True
    return flag, mychard[0]


# 6、顺子
def isShunZi(mychard):
    flag = False
    if len(mychard) >= 5:
        testStr = ""
        for item in mychard:
            testStr = testStr + item
        staight_str = "2AKQJ109876543"
        flag = testStr in staight_str
    return flag, mychard[0]


# 7、四带二
def isSiDaiEr(mychard):
    flag = False
    if len(mychard) == 6:
        # 有3种情况
        # 相同在列首
        if (mychard[0] == mychard[1] and mychard[1] == mychard[2] and mychard[2] == mychard[3] and mychard[
            3] != mychard[4]):
            flag = True
            return flag, mychard[0]
        # 在列中
        if (mychard[0] != mychard[1] and mychard[1] == mychard[2] and mychard[2] == mychard[3] and mychard[3] ==
            mychard[
                4] and mychard[4] != mychard[5]):
            flag = True
            return flag, mychard[1]

        # 在列尾
        if (mychard[2] == mychard[3] and mychard[3] == mychard[4] and mychard[4] == mychard[5] and mychard[1] !=
            mychard[
                2]):
            flag = True
            return flag, mychard[2]

    return flag, mychard[0]


# 8、连对
def isLianDui(mychard):
    flag = False
    chard_len = len(mychard)
    testStr = ''
    staight_str = "22AAKKQQJJ101099887766554433"
    if chard_len >= 6 and chard_len % 2 == 0:
        for item in mychard:
            testStr = testStr + item
        flag = testStr in staight_str
    return flag, mychard[0]


# 9、飞机不带
def isFeiJiBuDai(mychard):
    flag = False

    test_str = ""
    straight_str = "222AAAKKKQQQJJJ101010999888777666555444333"

    if len(mychard) >= 6 and len(mychard) % 3 == 0:
        for item in mychard:
            test_str = test_str + item
        flag = test_str in straight_str

    return flag, mychard[0]


# 10、飞机带单
def isFeiJiDaiDan(mychard):
    flag = False
    if len(mychard) >= 8 and len(mychard) % 4 == 0:
        # 用于判断3个是否为顺子
        test_str = ""
        straight_str = "2AKQJ109876543"
        # 用于判断带的个数是否正确
        count = 0

        # 保持顺序的数组去重
        func = lambda x, y: x if y in x else x + [y]
        single = reduce(func, [[], ] + mychard)

        # 计算数字重复格式
        c = Counter(mychard)

        for item in single:
            if c[item] == 3:
                test_str = test_str + item
                count = count + 1
        if test_str in straight_str and len(mychard) - count * 3 == count:
            flag = True
            return flag, test_str[0]
    return flag, mychard[0]


# 11、飞机带对子
def isFeiJiDaiDuiZi(mychard):
    flag = False
    if len(mychard) >= 10 and len(mychard) % 5 == 0:
        # 用于判断3个是否为顺子
        test_str = ""
        straight_str = "2AKQJ109876543"
        # 用于判断带的个数是否正确
        three_count = 0
        two_count = 0
        # 保持顺序的数组去重
        func = lambda x, y: x if y in x else x + [y]
        single = reduce(func, [[], ] + mychard)
        # 计算数字重复格式
        c = Counter(mychard)
        for item in single:
            if c[item] == 3:
                test_str = test_str + item
                three_count = three_count + 1
            if c[item] == 2:
                two_count = two_count + 1
        if test_str in straight_str and len(mychard) - three_count * 3 == two_count * 2:
            flag = True
            return flag, test_str[0]
    return flag, mychard[0]


# 11、王炸
def isWangZha(mychard):
    flag = False
    if len(mychard) == 2:
        if (mychard[0] == "Big" and mychard[1] == "Small") or (mychard[1] == "Big" and mychard[0] == "Small"):
            flag = True
    return flag, mychard[0]


# ["isDan","isDuiZi","isSanBuDai","isSanDaiYi","isSanDaiDuiZi","isBoom","isShunZi","isSiDaiEr","isLianDui",
#  isFeiJiBuDai(),isFeiJiDaiDan(),isFeiJiDaiDuiZi(),isWangZha()]

# test = [isDan(),isDuiZi(),isSanBuDai(),isSanDaiYi(),isSanDaiDuiZi(),isBoom(),isShunZi(),isSiDaiEr(),isLianDui(),
#  isFeiJiBuDai(),isFeiJiDaiDan(),isFeiJiDaiDuiZi(),isWangZha()]

# test = [isDan, isDuiZi, isSanBuDai, isSanDaiYi, isSanDaiDuiZi, isBoom, isShunZi, isSiDaiEr, isLianDui,
#         isFeiJiBuDai, isFeiJiDaiDan, isFeiJiDaiDuiZi, isWangZha]

card_types = {"isDan": isDan, "isDuiZi": isDuiZi, "isSanBuDai": isSanBuDai, "isSanDaiYi": isSanDaiYi,
              "isSanDaiDuiZi": isSanDaiDuiZi,
              "isBoom": isBoom, "isShunZi": isShunZi, "isSiDaiEr": isSiDaiEr, "isLianDui": isLianDui,
              "isFeiJiBuDai": isFeiJiBuDai,
              "isFeiJiDaiDan": isFeiJiDaiDan, "isFeiJiDaiDuiZi": isFeiJiDaiDuiZi, "isWangZha": isWangZha}


# 问题
def get_card_type(cards):
    for i in card_types:
        if card_types[i](cards)[0] is True:
            return i, card_types[i](cards)[1]
        else:
            pass
    return False, cards[0]


# 测试区


print get_card_type(["9","9","8", "8", "8", "7", "7", "7", "3", "3"])
print get_card_type([ "7", "7", "6", "6", "6", "6","3", "3"])
print get_card_type(['9', '8', '7', '6', '5', '4'])
print get_card_type(['8', '7', '6', '5', '4', '3'])
