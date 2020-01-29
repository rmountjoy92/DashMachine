from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField(validators=[DataRequired()])

    password = PasswordField(validators=[DataRequired()])

    confirm_password = PasswordField()

    remember = BooleanField()
