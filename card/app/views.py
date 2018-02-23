# encoding=utf-8
from flask import Flask, render_template, session, request, jsonify, g
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_socketio import SocketIO, join_room, send, leave_room, emit
from app import app, db, socketio
from models import User, Room, Role

# 判断牌型
from logic import get_card_type

import json
import random

# 生成牌
cardType = ("suitdiamonds", "suithearts", "suitclubs", "suitspades")
cardNum = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")


def generatecards():
    cardPairs = []  # 两层循环嵌套，生成52张花色牌，存入列表
    for type in cardType:
        for num in cardNum:
            cardPairs.append((type, num))

    # cardPairs.append(("Red", "Joker-R"))  # 大王
    # cardPairs.append(("Black", "Joker-B"))  # 小王
    cardPairs.append(("suitbig", "王"))  # 大王
    cardPairs.append(("suitsmall", "王"))  # 小王
    return cardPairs


# 牌值
dir = {"A": 20, "2": 30, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12,
       "K": 13, "王": 40, "王": 50}


# 排序
def select_sort(lists):
    # 选择排序
    count = len(lists)
    for i in range(0, count):
        max = i
        for j in range(i + 1, count):
            if dir[lists[max][1]] < dir[lists[j][1]]:
                max = j
        lists[max], lists[i] = lists[i], lists[max]
    return lists


@app.route('/')
@login_required
def index():
    nickname = g.user.name
    print nickname
    rooms = db.session.query(Room).filter(Room.count < 3).all()
    print rooms
    result = db.session.query(User).filter(User.name == nickname).first()
    print result.room_name
    return render_template('room.html', nickname=nickname, rooms=rooms, judge=result.room_name)


@app.route('/delRoom', methods=['GET', 'POST'])
def delRoom():
    nickname = g.user.name
    print nickname
    rooms = db.session.query(Room).filter(Room.count < 3).all()
    print rooms
    result = db.session.query(User).filter(User.name == nickname).first()
    roomName = result.room_name

    db.session.query(User).filter(User.room_name == roomName).update({'room_name': ''})
    db.session.query(Room).filter(Room.name == roomName).delete()
    db.session.commit()
    result = db.session.query(User).filter(User.name == nickname).first()
    print result.room_name, 2

    return render_template('room.html', nickname=nickname, rooms=rooms, judge=result.room_name)


# @app.before_first_request
# def create_user():
#     db.drop_all()
#     db.create_all()
#     user.create_user(email='a@b.c', password='password')
#     db.session.commit()
@app.route('/get_not_full_room', methods=['POST', "GEt"])
def get_not_full_room():
    records = db.session.query(Room).filter(Room.count < 3).all()
    return jsonify({"success": records})


@app.before_request
def before_request():
    g.user = current_user


@socketio.on('join')
def on_join(data):
    print 'join'
    room = data['room']
    password = data['password']
    username = data['username']

    # 查看是否存在该房间
    records = len(db.session.query(Room).filter(Room.name == room).all())

    if records != 0:
        emit('my_response', {'status': 'sorry', 'msg': u'这个房间已经存在'})
    else:
        room_record = Room(name=room, password=password, count=1)
        db.session.add(room_record)
        db.session.query(User).filter(User.name == username).update({'number': 1, "room_name": room})
        db.session.commit()
        join_room(room)

        # 查询用户信息，还原状态
        users = db.session.query(User).filter(User.room_name == room).all()

        user_arr = []
        for user in users:
            print user.name
            item = {}
            item['name'] = user.name
            item['number'] = user.number
            item['prepare'] = user.prepare
            item['cards'] = user.cards
            user_arr.append(item)

        print user_arr

        # emit('my_response', {'status': 'succeed','judge': 'join_room_success','msg':u'test', 'data': username}, room=room)
        # emit('my_response', {'status': 'success', 'judge': 'join_room_success', 'msg': u'房间创建成功'}, room=room)
        # u'房间：' + room + u'创建成功
        emit('my_response', {'status': 'success', 'judge': 'join_room_success', 'msg': u'房间创建成功的消息再次发生', 'data': 1})
        emit('join_response', {'status': 'success', 'judge': 'join_room_success', 'msg': u'用户信息已更新',
                               'userInfo': user_arr},
             room=room)


# @socketio.on('join')
# def on_join(data):
#     print "join"
#     # username = g.user.name
#     # print current_user.name
#     # print 'gurrent_user.name'
#     # print g.user
#     # us = current_user.name
#
#     # username = data['username']
#     print 'username', username
#     room = data['room']
#     password = data['password']
#
#     print "success"
#
#     records = len(db.session.query(Room).filter(Room.name == room).all())
#
#     # 判断是否有这个房间存在,不存在则创建，已有就验证进入
#     if records == 0:
#         print "test"
#         room_record = Room(name=room, password=password, count=1)
#         # user_record = User(name=username, number=1, room_name=room)
#         db.session.add(room_record)
#         db.session.query(User.name == username).update({'number': 1, "room_name": room})
#         db.session.commit()
#         join_room(room)
#         print room
#         # send(username + ' has entered the room.', room=room)
#         emit('my_response', {'data': 'username'}, room=room)
#     elif records == 1:
#         user_count = len(db.session.query(User).filter(User.room_name == room).all())
#
#         if password == db.session.query(Room).filter(Room.name == room).first().password:
#             #         当房间存在时，查看房间里的人数，未满3人。则加入房间，已满无法加入
#             if user_count < 3:
#                 db.session.query(Room).filter(Room.name == room).update({'count': user_count + 1})
#                 # user_record = User(name=username, number=user_count + 1, room_name=room)
#                 db.session.query(User.name == username).update({'number': user_count + 1, "room_name": room})
#                 # db.session.add(user_record)
#                 db.session.commit()
#                 join_room(room)
#                 print room
#                 emit('my_response', {'data': username}, room=room)
#             else:
#                 # 当房间人数达到3人时，查看用户是否是该房间成员，如果是该成员可以进入
#                 #####################           是否添加密码验证用户？？？                      ###################
#                 # 异常处理查看是否有该成员
#                 try:
#                     result = db.session.query(User).filter((User.name == username) & (User.room_name == room)).all()
#                     print '查看是否有该成员', result
#                 except:
#                     #  没有则表示房间已满，无法进入
#                     emit('my_response', {'data': 'The room is full!'})
#                 else:
#                     emit('my_response', {'data': username}, room=room)
#         else:
#             #  进入房间的密码不对
#             emit('my_response', {'data': 'The room password is wrong'})
#     else:
#         #     存在两个相同的房间号时
#         emit('my_response', {'data': 'Please choose another rooms'})

@socketio.on('selectJoin')
def selectJoin(data):
    print 'selectJoin'
    room = data['room']
    password = data['password']
    username = data['username']
    print room, password, username

    user_count = len(db.session.query(User).filter(User.room_name == room).all())
    print user_count
    print db.session.query(Room).filter(Room.name == room).first().password
    if password == db.session.query(Room).filter(Room.name == room).first().password:
        #         当房间存在时，查看房间里的人数，未满3人。则加入房间，已满无法加入
        print 'success'

        if user_count < 3:
            db.session.query(Room).filter(Room.name == room).update({'count': user_count + 1})
            # user_record = User(name=username, number=user_count + 1, room_name=room)
            db.session.query(User).filter(User.name == username).update({'number': user_count + 1, "room_name": room})
            # db.session.add(user_record)
            db.session.commit()
            join_room(room)
            print room

            # 查询用户信息，还原状态
            users = db.session.query(User).filter(User.room_name == room).all()

            user_arr = []
            number = 0
            for user in users:
                item = {}
                item['name'] = user.name
                item['number'] = user.number
                item['prepare'] = user.prepare
                item['cards'] = user.cards
                user_arr.append(item)
                if user.name == username:
                    number = user.number
                else:
                    pass

            print user_arr, 'user_arr+select_join'
            emit('my_response', {'status': 'success', 'judge': 'join_room_success', 'msg': u'您已进入房间', 'data': number
                                 })
            emit('join_response',
                 {'status': 'success', 'judge': 'join_room_success', 'msg': u'用户信息已更新',
                  'userInfo': user_arr},
                 room=room)
        else:
            # 当房间人数达到3人时，查看用户是否是该房间成员，如果是该成员可以进入
            #####################           是否添加密码验证用户？？？                      ###################
            # 异常处理查看是否有该成员
            result = db.session.query(User).filter((User.name == username) & (User.room_name == room)).all()

            print '查看是否有该成员', result
            if len(result) == 1:
                seat_num = result[0].number
                join_room(room)

                # 查询用户信息，还原状态
                users = db.session.query(User).filter(User.room_name == room).all()

                user_arr = []
                for user in users:
                    item = {}
                    item['name'] = user.name
                    item['number'] = user.number
                    item['prepare'] = user.prepare
                    item['cards'] = user.cards
                    user_arr.append(item)
                print user_arr, 'user_arr+select_join 已满3人情况'
                emit('my_response',
                     {'status': 'success', 'judge': 'join_room_success', 'msg': u'您已回到房间', 'data': seat_num
                      })
                emit('join_response',
                     {'status': 'success', 'judge': 'join_room_success', 'msg': u'用户信息已更新',
                      'userInfo': user_arr}, room=room)
            else:
                emit('my_response', {'status': 'success', 'judge': 'join_room_unsuccess', 'msg': u'该房间已满'})


@socketio.on('back_room')
def back_room(data):
    print 'back_room'
    username = data['username']
    room = data['room']
    # number = db.session.query(User).filter(User.name == username).first().number
    # allcards = db.session.query(Room).filter(Room.name == room).first().allCards

    # 查询用户信息，还原状态
    users = db.session.query(User).filter(User.room_name == room).all()

    user_arr = []
    number = 0
    for user in users:
        print user.name
        item = {}
        item['name'] = user.name
        item['number'] = user.number
        item['prepare'] = user.prepare
        item['cards'] = user.cards
        user_arr.append(item)
        if user.name == username:
            number = user.number
        else:
            pass

    print user_arr, 'back_home'
    join_room(room)
    emit('my_response',
         {'status': 'success', 'judge': 'join_room_success',
          'msg': u'您已回到房间', 'data': number})
    emit('join_response',
         {'status': 'success', 'judge': 'join_room_success',
          'msg': u'用户信息已更新', 'userInfo': user_arr},
         room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print room
    print 'leave room' * 5
    # send(username + ' has left the room.', room=room)
    emit('my_response', {'data': username}, room=room)


@socketio.on('my_room_event')
def send_room_message(message):
    print "send_room_message"
    print message
    emit('my_response',
         {'data': message['data']},
         room=message['room'])


# 用户准备
@socketio.on('user_prepare')
def user_prepared(message):
    # room = message['room']
    username = message['username']
    # db.session.query(User).filter((User.name == username) & (User.room_name == room)).update({'prepare': True})
    # print room
    db.session.query(User).filter(User.name == username).update({'prepare': True})
    db.session.commit()
    room = db.session.query(User).filter(User.name == username).first().room_name
    records = db.session.query(User).filter((User.room_name == room) & (User.prepare == True)).all()
    print len(records)

    if len(records) == 3:
        # 当3人都准备好时，则生成牌，放入数据库中。这样可以死保证拿到的是一副牌

        #
        # 生成牌
        cardPairs = generatecards()

        # 分配牌
        random.shuffle(cardPairs)
        # 玩家手牌
        player1Cards = []
        player2Cards = []
        player3Cards = []
        coverCardNum = 3  # 3张底牌
        for index in range(0, len(cardPairs) - coverCardNum):
            cardPair = cardPairs[index]
            if index % 3 == 0:  # player1
                player1Cards.append(cardPair)
            elif index % 3 == 1:  # player2
                player2Cards.append(cardPair)
            else:  # player3
                player3Cards.append(cardPair)

        rest_cards = cardPairs[-3:]  # 剩余三张牌

        rest_cards = select_sort(rest_cards)
        player3Cards = select_sort(player3Cards)
        player2Cards = select_sort(player2Cards)
        player1Cards = select_sort(player1Cards)

        # 随机数，随机到的先叫地主
        king = random.randint(1, 3)
        print king

        cards_json = {"player1Cards": player1Cards, "player2Cards": player2Cards, "player3Cards": player3Cards,
                      'finalCards': rest_cards,'king':king}

        cards_str = json.dumps(cards_json)
        # 将牌组转成字符串存入数组中
        # db.session.query(Room).filter(Room.name == room).update(
        #     {'player1Cards': str(player1Cards), 'player2Cards': str(player2Cards), 'player3Cards': str(player3Cards),
        #      'finalCards': str(rest_cards)})
        db.session.query(Room).filter(Room.name == room).update({'allCards': cards_str})

        emit('my_response',
             {'status': 'success', 'judge': 'prepare',
              'msg': u'开始发牌','data': 'waiting for cards'}, room=room)
        # emit('my_response', {'data': 'waiting for cards'}, room=room)
    else:
        emit('my_response',
             {'status': 'success', 'judge': 'prepare',
              'msg': u'请等待其他人准备'}, room=room)
        # emit('my_response', {'data': 'Please wait for others to prepare' + str(len(records))})


# 发牌
@socketio.on('get_cards')
def get_cards(message):
    print "get_cards"

    # 根据房间号，从数组中取出牌组传给前台
    username = message['username']
    room = db.session.query(User).filter(User.name == username).first().room_name
    record = db.session.query(User).filter(User.name == username and User.room_name == room).first()
    card_record = db.session.query(Room).filter(Room.name == room).first()
    cards_str = card_record.allCards
    cards_json = json.loads(cards_str)
    print record.number


    print cards_json
    if (record.number == 1):
        emit('card_response',
             {'code': 'success', 'card': cards_json["player1Cards"], 'final_cards': cards_json["finalCards"],
              'right_cards_num': 17,
              'left_cards_num':
                  17})
    elif (record.number == 2):
        emit('card_response',
             {'code': 'success', 'card': cards_json["player2Cards"], 'final_cards': cards_json["finalCards"],
              'right_cards_num': 17,
              'left_cards_num':
                  17})
    elif (record.number == 3):
        emit('card_response',
             {'code': 'success', 'card': cards_json["player3Cards"], 'final_cards': cards_json["finalCards"],
              'right_cards_num': 17,
              'left_cards_num':
                  17})
    # if (record.number == 1):
    #     emit('card_response',
    #          {'code': 'success', 'card': card_record.player1Cards, 'final_cards': card_record.finalCards,
    #           'right_cards_num': 17,
    #           'left_cards_num':
    #               17})
    # elif (record.number == 2):
    #     emit('card_response',
    #          {'code': 'success', 'card': card_record.player2Cards, 'final_cards': card_record.finalCards,
    #           'right_cards_num': 17,
    #           'left_cards_num':
    #               17})
    # elif (record.number == 3):
    #     emit('card_response',
    #          {'code': 'success', 'card': card_record.player3Cards, 'final_cards': card_record.finalCards,
    #           'right_cards_num': 17,
    #           'left_cards_num':
    #               17})
    else:
        emit('card_response', {'code': 'ubsuccess', 'msg': 'There are bugs here'})


# 出牌
@socketio.on('send_cards')
def send_cards(message):
    print "send_cards"

    # 根据房间号，从数组中取出牌组传给前台
    username = message['username']
    sendCards = message['sendCards']
    print sendCards
    # 打印牌型
    print get_card_type(sendCards)
    emit('my_response', {'msg': 'you can play'})



# 客户端连接上服务端
@socketio.on('connect')
def test_connect():
    print('Client connected', request.sid)
    emit('my_response', {'data': 'Connected', 'count': 0})


# 客户端断开连接
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)
