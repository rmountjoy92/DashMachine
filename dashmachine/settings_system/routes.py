import os
from shutil import move
from configparser import ConfigParser
from flask_login import current_user
from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from dashmachine.user_system.forms import UserForm
from dashmachine.user_system.models import User
from dashmachine.main.utils import public_route, check_groups
from dashmachine.main.read_config import read_config
from dashmachine.main.models import Files
from dashmachine.settings_system.forms import ConfigForm
from dashmachine.settings_system.utils import load_files_html, get_config_html
from dashmachine.settings_system.models import Settings
from dashmachine.paths import (
    backgrounds_images_folder,
    icons_images_folder,
    user_data_folder,
    template_apps_folder,
)
from dashmachine.version import version

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
    config = ConfigParser()
    for template_app_ini in os.listdir(template_apps_folder):
        config.read(os.path.join(template_apps_folder, template_app_ini))
        entry = config[template_app_ini.replace(".ini", "")]
        template_apps.append(f"{template_app_ini.replace('.ini', '')}&&{entry['icon']}")

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
    fn = os.path.join(template_apps_folder, f"{request.args.get('name')}.ini")
    with open(fn, "r") as template_app_ini:
        template = template_app_ini.read().replace("\n", "<br>")
    return template
