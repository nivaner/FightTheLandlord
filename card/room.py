# encoding=utf-8
from flask import Flask, render_template, session, request, jsonify,g
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_session import Session
from flask_socketio import SocketIO, join_room, send, leave_room, emit
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from wtforms.fields import  StringField, DateTimeField, SubmitField, DateField,TextAreaField
from flask_security.forms import RegisterForm,Required



import json
import random
import time

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


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
Session(app)
socketio = SocketIO(app, manage_session=False)
manage = Manager(app)


# model
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Room(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    count = db.Column(db.Integer())
    allCards = db.Column(db.Text())
    # player1Cards = db.Column(db.Text())
    # player2Cards = db.Column(db.Text())
    # player3Cards = db.Column(db.Text())
    # finalCards = db.Column(db.Text())
    user = db.relationship('User', backref='users')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255), unique=True)
    number = db.Column(db.Integer())
    room_name = db.Column(db.String(256), db.ForeignKey('room.name'))
    prepare = db.Column(db.Boolean())
    cards = db.Column(db.Text())
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class ExtendedRegisterForm(RegisterForm):
    name = StringField('nickname', [Required()])



# class Cards(db.Model):
#     id = db.Column(db.Integer(),primary_key=True)
#     play1Cards = db.Column(db.Text())
#     play2Cards = db.Column(db.Text())
#     Play3Cards = db.Column(db.Text())
#     finalCards = db.Column(db.Text())
#     room_name = db.Column(db.String(255), unique=True)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,
         register_form=ExtendedRegisterForm)



@app.route('/')
@login_required
def index():
    return render_template('room.html')

@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()
    user_datastore.create_user(email='a@b.c', password='password')
    db.session.commit()

@app.before_request
def before_request():
    g.user = current_user
    print g.user,"当前人员"
    print "----------*test*--------------"

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    password = data['password']

    print "success"

    records = len(db.session.query(Room).filter(Room.name == room).all())

    # 判断是否有这个房间存在,不存在则创建，已有就验证进入
    if records == 0:
        print "test"
        room_record = Room(name=room, password=password, count=1)
        user_record = User(name=username, number=1, room_name=room)
        db.session.add(room_record)
        db.session.add(user_record)
        db.session.commit()
        join_room(room)
        print room
        # send(username + ' has entered the room.', room=room)
        emit('my_response', {'data': 'username'}, room=room)
    elif records == 1:
        user_count = len(db.session.query(User).filter(User.room_name == room).all())

        if password == db.session.query(Room).filter(Room.name == room).first().password:
            #         当房间存在时，查看房间里的人数，未满3人则加入房间，已满无法加入
            if user_count < 3:
                db.session.query(Room).filter(Room.name == room).update({'count': user_count + 1})
                user_record = User(name=username, number=user_count + 1, room_name=room)
                db.session.add(user_record)
                db.session.commit()
                join_room(room)
                print room
                emit('my_response', {'data': username}, room=room)
            else:
                # 当房间人数达到3人时，查看用户是否是该房间成员，如果是该成员可以进入
       #####################           是否添加密码验证用户？？？                      ###################
                # 异常处理查看是否有该成员
                try:
                    result = db.session.query(User).filter((User.name == username) & (User.room_name == room)).all()
                    print '查看是否有该成员',result
                except:
                    #  没有则表示房间已满，无法进入
                    emit('my_response', {'data': 'The room is full!'})
                else:
                    emit('my_response', {'data': username}, room=room)
        else:
            #  进入房间的密码不对
            emit('my_response', {'data': 'The room password is wrong'})
    else:
        #     存在两个相同的房间号时
        emit('my_response', {'data': 'Please choose another rooms'})


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print room
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
    room = message['room']
    username = message['username']
    db.session.query(User).filter((User.name == username) & (User.room_name == room)).update({'prepare': True})
    print room
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

        cards_json = {"player1Cards": player1Cards, "player2Cards": player2Cards, "player3Cards": player3Cards,
                      'finalCards': rest_cards}

        cards_str = json.dumps(cards_json)
        # 将牌组转成字符串存入数组中
        # db.session.query(Room).filter(Room.name == room).update(
        #     {'player1Cards': str(player1Cards), 'player2Cards': str(player2Cards), 'player3Cards': str(player3Cards),
        #      'finalCards': str(rest_cards)})
        db.session.query(Room).filter(Room.name == room).update({'allCards': cards_str})

        emit('my_response', {'data': 'waiting for cards'}, room=message['room'])
    else:
        emit('my_response', {'data': 'Please wait for others to prepare' + str(len(records))})


# 发牌
@socketio.on('get_cards')
def get_cards(message):
    print "get_cards"

    # 根据房间号，从数组中取出牌组传给前台
    username = message['username']
    room = message['room']
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


# 客户端连接上服务端
@socketio.on('connect')
def test_connect():
    print('Client connected', request.sid)
    emit('my_response', {'data': 'Connected', 'count': 0})


# 客户端断开连接
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    # manage.run()
    # app.run(debug=True, host='0.0.0.0')