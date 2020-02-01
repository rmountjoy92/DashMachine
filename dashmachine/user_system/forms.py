from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=4, max=120)])

    password = PasswordField(validators=[DataRequired(), Length(min=8, max=120)])

    confirm_password = PasswordField()

    remember = BooleanField()
