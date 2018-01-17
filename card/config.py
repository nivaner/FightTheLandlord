import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'super-secret-you-will-never-hack'
SESSION_TYPE = 'filesystem'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'card.db')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECURITY_MAIL_SENDER = "1964893266@qq.com"
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'AIPatent2016'

