# encoding=utf-8
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from app import db

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