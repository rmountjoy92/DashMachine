from flask import render_template, url_for, redirect, Blueprint
from flask_login import login_user, logout_user, current_user
from dashmachine.user_system.forms import UserForm
from dashmachine.user_system.models import User
from dashmachine.user_system.utils import add_edit_user
from dashmachine import bcrypt
from dashmachine.main.utils import public_route

user_system = Blueprint("user_system", __name__)


# ------------------------------------------------------------------------------
# User system routes
# ------------------------------------------------------------------------------
# login page
@public_route
@user_system.route("/login", methods=["GET", "POST"])
def login():
    user = User.query.first()

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = UserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            return redirect(url_for("main.home"))

        else:
            print("password was wrong")
            return redirect(url_for("user_system.login"))

    return render_template("user/login.html", title="Login", form=form)


# this logs the user out and redirects to the login page
@user_system.route("/logout")
def logout():

    logout_user()
    return redirect(url_for("user_system.login"))


@user_system.route("/edit_user", methods=["POST"])
def edit_user():
    form = UserForm()

    if form.validate_on_submit():
        add_edit_user(username=form.username.data, password=form.password.data)

    return 'ok'