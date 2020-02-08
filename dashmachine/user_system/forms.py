from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from dashmachine.settings_system.models import Settings

settings_db = Settings.query.first()


class UserForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=120)])

    password = PasswordField(validators=[DataRequired(), Length(min=8, max=120)])

    role = SelectField(choices=[(role, role) for role in settings_db.roles.split(",")])

    id = StringField()

    confirm_password = PasswordField()


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=120)])

    password = PasswordField(validators=[DataRequired(), Length(min=8, max=120)])

    remember = BooleanField()
