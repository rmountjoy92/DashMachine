import os
from shutil import move
from flask_login import current_user
from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from dashmachine.user_system.forms import UserForm
from dashmachine.user_system.utils import add_edit_user
from dashmachine.user_system.models import User
from dashmachine.main.utils import row2dict, public_route, check_groups
from dashmachine.main.read_config import read_config
from dashmachine.main.models import Files, TemplateApps
from dashmachine.settings_system.forms import ConfigForm
from dashmachine.settings_system.utils import load_files_html, get_config_html
from dashmachine.settings_system.models import Settings
from dashmachine.paths import (
    backgrounds_images_folder,
    icons_images_folder,
    user_data_folder,
)
from dashmachine.version import version
from dashmachine import db

settings_system = Blueprint("settings_system", __name__)


@public_route
@settings_system.route("/settings", methods=["GET"])
def settings():
    settings_db = Settings.query.first()
    if not check_groups(settings_db.settings_access_groups, current_user):
        return redirect(url_for("main.home"))

    config_form = ConfigForm()
    user_form = UserForm()
    user_form.role.choices += [(role, role) for role in settings_db.roles.split(",")]
    with open(os.path.join(user_data_folder, "config.ini"), "r") as config_file:
        config_form.config.data = config_file.read()
    files_html = load_files_html()
    template_apps = []
    t_apps = TemplateApps.query.all()
    for t_app in t_apps:
        template_apps.append(f"{t_app.name}&&{t_app.icon}")

    users = User.query.all()
    config_readme = get_config_html()
    return render_template(
        "settings_system/settings.html",
        config_form=config_form,
        files_html=files_html,
        user_form=user_form,
        template_apps=",".join(template_apps),
        version=version,
        users=users,
        config_readme=config_readme,
    )


@settings_system.route("/settings/save_config", methods=["POST"])
def save_config():
    with open(os.path.join(user_data_folder, "config.ini"), "w") as config_file:
        config_file.write(request.form.get("config"))
    msg = read_config()
    return jsonify(data=msg)


@settings_system.route("/settings/add_images", methods=["POST"])
def add_images():
    if request.form.get("folder") == "icons":
        dest_folder = icons_images_folder
    elif request.form.get("folder") == "backgrounds":
        dest_folder = backgrounds_images_folder
    for cached_file in request.form.get("files").split(","):
        file = Files.query.filter_by(cache=cached_file).first()
        new_path = os.path.join(dest_folder, file.name)
        move(file.path, new_path)
    return load_files_html()


@settings_system.route("/settings/delete_file", methods=["GET"])
def delete_file():
    if request.args.get("folder") == "backgrounds":
        file = os.path.join(backgrounds_images_folder, request.args.get("file"))
    if request.args.get("folder") == "icons":
        file = os.path.join(icons_images_folder, request.args.get("file"))
    os.remove(file)
    return load_files_html()


@settings_system.route("/settings/get_app_template", methods=["GET"])
def get_app_template():
    template_app = TemplateApps.query.filter_by(name=request.args.get("name")).first()
    template = f"[{template_app.name}]<br>"
    for key, value in row2dict(template_app).items():
        if key not in ["id", "name"]:
            template += f"{key} = {value}<br>"
    return template


@settings_system.route("/settings/edit_user", methods=["POST"])
def edit_user():
    form = UserForm()
    settings_db = Settings.query.first()
    form.role.choices += [(role, role) for role in settings_db.roles.split(",")]
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            return jsonify(data={"err": "Passwords don't match"})
        err = add_edit_user(
            form.username.data,
            form.password.data,
            user_id=form.id.data,
            role=form.role.data,
        )
        if err:
            return jsonify(data={"err": err})
    else:
        err_str = ""
        for fieldName, errorMessages in form.errors.items():
            err_str += f"{fieldName}: "
            for err in errorMessages:
                err_str += f"{err} "
        return jsonify(data={"err": err_str})
    users = User.query.all()
    html = render_template("settings_system/user.html", users=users)
    return jsonify(data={"err": "success", "html": html})


@settings_system.route("/settings/delete_user", methods=["GET"])
def delete_user():
    admin_users = User.query.filter_by(role="admin").all()
    user = User.query.filter_by(id=request.args.get("id")).first()
    if len(admin_users) < 2 and user.role == "admin":
        return jsonify(data={"err": "You must have at least one admin user"})
    else:
        User.query.filter_by(id=request.args.get("id")).delete()
    db.session.commit()
    users = User.query.all()
    html = render_template("settings_system/user.html", users=users)
    return jsonify(data={"err": "success", "html": html})
