# encoding=utf-8
from wtforms.fields import StringField, DateTimeField, SubmitField, DateField, TextAreaField
from flask_security.forms import RegisterForm, Required


class ExtendedRegisterForm(RegisterForm):
    name = StringField('nickname', [Required()])
