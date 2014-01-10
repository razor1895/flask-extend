# -*- coding: utf-8 -*-
import re
from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from models import User
from hashlib import md5


class RegisterFrom(Form):
    nickname = TextField('nickname', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    conform = PasswordField('conform', validators=[DataRequired()])


    def validate_nickname(self, field):
        nickname = field.data.strip()
        if len(nickname) < 3 or len(nickname) > 20:
            raise ValidationError('nickname must be 3 letter at least')
        elif not re.search(r'^\w+$', nickname):
            raise ValidationError('User names can contain only alphanumeric characters and underscores.')
        else:
            u = User.query.filter_by(nickname=nickname).first()
            if u:
                raise ValidationError('The nickname already exists')

    def validate_email(self, field):
        email = field.data.strip()
        email  = User.query.filter_by(email=email).first()
        if email:
            raise ValidationError('The email already exists')

    def validate_password(self, field):
        password = field.data.strip()
        if len(password) < 6:
            raise ValidationError('password must be 3 letter at least')

    def validate_conform(self, field):
        conform = field.data.strip()
        if self.data['password'] != conform:
            raise ValidationError('the password and conform are different')

class LoginForm(Form):
    nickname = TextField('nickname', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

    def validate_nickname(self, field):
        nickname = field.data.strip()
        if len(nickname) < 3 or len(nickname) > 20:
            raise ValidationError('nickname must be 3 letter at least')
        elif not re.search(r'^\w+$', nickname):
            raise ValidationError('User names can contain only alphanumeric characters and underscores.')
        else:
            return nickname