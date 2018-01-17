#-*- coding: utf-8 -*
import random
import time

cardType = ("hei","hong","mei","fang")
cardNum = ("A","2","3","4","5","6","7","8","9","10","J","Q","K")


def generatecards():
    cardPairs = []  #两层循环嵌套，生成52张花色牌，存入列表
    for type in cardType:
        for num in cardNum:
            cardPairs.append((type,num))

    cardPairs.append(("Joker","Red"))  #大王
    cardPairs.append(("Joker", "Black"))  # 小王
    return cardPairs

# def dispatchcards(cardPairs):
    #洗牌 - 多次调用
    random.shuffle(cardPairs)
    random.shuffle(cardPairs)
    #玩家手牌
    player1Cards = []
    player2Cards = []
    player3Cards = []
    coverCardNum = 3   #3张底牌
    for index in range(0,len(cardPairs) - coverCardNum):
        cardPair = cardPairs[index]
        if index % 3 == 0:  #player1
            player1Cards.append(cardPair)
            print
        elif index % 3 == 1:  #player2
            player2Cards.append(cardPair)
        else:   #player3
            player3Cards.append(cardPair)
        print ''.join(cardPair),'\t\t',  #模拟发牌效果，输出当前发出的牌
        time.sleep(0.1)  #发牌停顿
    # print '\n'

    # print u"玩家1 手牌：",len(player1Cards)
    # for cardPair in player1Cards:
    #     print ''.join(cardPair)
    # print
    #
    # print u'玩家2 手牌：',len(player2Cards)
    # for cardPair in player2Cards:
    #     print ''.join(cardPair)
    # print
    #
    # print u"玩家3 手牌",len(player3Cards)
    # for cardPair in player3Cards:
    #     print ''.join(cardPair)
    # print

    # print u'底牌:'
    # rest_cards = cardPairs[-3:] #剩余三张牌
    # for card in rest_cards:
    #     print ''.join(card)

# if __name__ == '__main__':
        生成牌o
    # cardPairs = generatecards()
        分配牌
    # dispatchcards(cardPairs)
