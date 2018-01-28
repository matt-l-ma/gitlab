# -*- coding:utf-8 -*-

from wtforms import form, fields, validators
from .. import db
from ..models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField

class LoginForm(form.Form):
    username = fields.StringField(u'用户名', validators=[validators.required()])
    password = fields.PasswordField(u'密码', validators=[validators.required()])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError(u'用户名不存在')

        if not user.password == self.password.data:
            raise validators.ValidationError(u'密码错误')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()
