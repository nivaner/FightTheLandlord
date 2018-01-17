# encoding=utf-8
from flask import Flask, render_template, session, request, jsonify, g
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_session import Session
from flask_socketio import SocketIO, join_room, send, leave_room, emit
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from wtforms.fields import StringField, DateTimeField, SubmitField, DateField, TextAreaField
from flask_security.forms import RegisterForm, Required
from forms import ExtendedRegisterForm

import json
import random
import time

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
Session(app)
socketio = SocketIO(app, manage_session=False)
manage = Manager(app)

from app import views
from models import  User, Role,Room
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app,user_datastore)
security = Security(app, user_datastore,
                    register_form=ExtendedRegisterForm)


