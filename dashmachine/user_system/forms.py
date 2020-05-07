from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=120)])

    password = PasswordField(validators=[DataRequired(), Length(min=8, max=120)])

    role = SelectField(choices=[])

    id = StringField()

    confirm_password = PasswordField()


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={"autofocus": True})

    password = PasswordField(validators=[DataRequired()])

    remember = BooleanField()
