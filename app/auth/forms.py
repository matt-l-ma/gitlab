from wtforms import form, fields, validators
from .. import db
from ..models import User

class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not user.password == self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()
