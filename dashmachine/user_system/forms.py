from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    FileField,
)
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from dashmachine.user_system.models import User


class PasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters."),
            EqualTo("confirm_password", message="Passwords must match."),
        ],
    )

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    def validate_email(form, field):
        if field.data == current_user.email:
            email_in_db = None
        else:
            email_in_db = User.query.filter_by(email=field.data).first()
        if email_in_db:
            raise ValidationError("Email is already registered.")

    fname = StringField("First Name", validators=[DataRequired()])

    lname = StringField("Last Name", validators=[DataRequired()])

    phone = StringField("Phone Number", validators=[DataRequired()])

    company = StringField("Company/Team Name")

    avatar = FileField()

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters."),
            EqualTo("confirm_password", message="Passwords must match."),
        ],
    )

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField("User Name", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField()

    remember = BooleanField("Remember Me")
