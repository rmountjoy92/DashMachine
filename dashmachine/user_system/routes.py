from flask import render_template, url_for, redirect, Blueprint, jsonify
from flask_login import login_user, logout_user
from dashmachine.user_system.forms import LoginForm
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
@user_system.route("/login", methods=["GET"])
def login():
    form = LoginForm()
    return render_template("user/login.html", title="Login", form=form)


@public_route
@user_system.route("/check_login", methods=["POST"])
def check_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if not user:
            response = {"err": "User not found"}

        elif bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            response = {"url": url_for("main.home")}
        else:
            response = {"err": "Password is wrong"}
    else:
        response = {"err": str(form.errors)}

    return jsonify(data=response)


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

    return "ok"
