from flask import Flask, render_template,flash, request,redirect,url_for,g
from flask_login import login_required,current_user, LoginManager,UserMixin
from room import db,User

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager(app)

@app.before_request
def before_request():
    g.user = current_user

# class User(db.Model):
#     __tablename__ = 'User'
#     UserID = db.Column(db.Integer, primary_key=True)
#     UserName = db.Column(db.String(15))
#     UserEmail = db.Column(db.String(45))
#     UserTEL = db.Column(db.String(11))
#     UserPassword = db.Column(db.String(200))
#     UserType = db.Column(db.Enum("Consumer", "Designer", "Company"), default="Consumer")
#     UserImage = db.Column(db.BLOB)
#     UserConfirm = db.Column(db.Boolean, default=False)
#
#     def __init__(self, name, email, pwd, type_, confirm):
#         self.UserEmail = email
#         self.UserName = name
#         self.UserPassword = generate_password_hash(pwd)
#         self.UserType = type_
#         self.UserConfirm = confirm
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         try:
#             return unicode(self.UserID)  # python 2
#         except NameError:
#             return str(self.UserID)  # python 3
#
#     def __repr__(self):
#         return '<User %r %d>' % (self.UserName, self.UserID)

# def login_func(email, password):
#     user = User.query.filter_by(UserEmail=email).first()
#     if user == None:
#         return "NOACCOUNT"
#     else:
#         if check_password_hash(user.UserPassword, password):
#             login_user(user)
#             session['userid'] = user.UserID
#             session['usertype'] = user.UserType
#             return "SUCCEED"
#         else:
#             return "WRONGPWD"

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/')
@login_required
def home():
    return 'test'

if __name__ == "__main__":
    app.run()




