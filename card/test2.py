# coding=utf-8
import random;

# num 可以修改顺序  已达到改变牌大小
num = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'k', 'A', '2'];
color = ['♠', '❤', '♣', '♢'];
kings = ["Big", "Small"];
list = [];
keep = [];
# 0~12 13*4=52  52+2(两张鬼牌)=54
for a in range(0, 53):
    # a=50  实际上是 52张牌
    list.append(a);

# 随机打乱顺序
random.shuffle(list);


# print("打乱顺序:",end='');

# print(list);

# 添加到玩家的手牌中
def inPlayer(b, number):
    count = number // 4;
    yu = number % 4;
    a = [];
    # 49 和50 代表是鬼牌
    if (number == 49):
        a.append(13);
        a.append(0);
    elif (number == 50):
        a.append(13);
        a.append(1);
    else:
        a.append(count);
        a.append(yu);
    b.append(a);


for a in range(0, 3):
    this = list[a];
    inPlayer(keep, this);

# 玩家一
one = [];
# 玩家二
two = [];
# 玩家三
three = [];

# 分牌
for i in range(3, list.__len__()):
    p = i % 3;
    number = list[i];
    if (p == 0):
        inPlayer(one, number);
        continue;
    if (p == 1):
        inPlayer(two, number);
        continue;
    if (p == 2):
        inPlayer(three, number);
        continue;


# 快速排序
# define a function
def quick(a, left, right):
    if (left >= right):
        return
    else:
        key = a[left];
        low = left;
        high = right;
        while (left < right):
            while (left < right and a[right] >= key):
                right -= 1;

            a[left] = a[right];
            while (left < right and a[left] <= key):
                left += 1;

            a[right] = a[left];

        a[left] = key;

        quick(a, low, left - 1);
        quick(a, left + 1, high);


quick(keep, 0, keep.__len__() - 1);
quick(one, 0, one.__len__() - 1)
quick(two, 0, two.__len__() - 1)
quick(three, 0, three.__len__() - 1)


def changeText(a):
    for i in range(0, a.__len__()):
        if (a[i][0] == 13):
            if (a[i][1] == 0):
                a[i] = kings[1];
            else:
                a[i] = kings[0];
        else:
            a[i] = str(num[a[i][0]]) + str(color[a[i][1]]);


changeText(keep);
changeText(one);
changeText(two);
changeText(three);

# print("地主牌", end=' ');
print(keep);
# print("第一位玩家", end=' ');
print(one);
# print("第二位玩家", end=' ');
print(two);
# print("第三位玩家", end=' ');
print(three);
