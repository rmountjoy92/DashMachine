import os
from shutil import move
from flask import (
    request,
    Blueprint,
    jsonify,
    render_template_string,
)
from dashmachine.main.read_config import read_config
from dashmachine.main.models import Files
from dashmachine.settings_system.utils import load_files_html
from dashmachine.paths import (
    backgrounds_images_folder,
    icons_images_folder,
    user_data_folder,
    template_apps_folder,
)

settings_system = Blueprint("settings_system", __name__)


@settings_system.route("/get_settings_data", methods=["GET"])
def get_settings_data():
    html = render_template_string(
        """
        {% from "main/base.html" import SettingsData with context%}
        {{ SettingsData() }}
        """
    )
    return html


@settings_system.route("/settings/save_config", methods=["POST"])
def save_config():
    with open(os.path.join(user_data_folder, "config.ini"), "w") as config_file:
        config_file.write(request.form.get("config"))
    msg = read_config()
    if msg["msg"] != "success":
        read_config(from_backup=True)
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
