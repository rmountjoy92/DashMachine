import os
from flask import render_template, url_for, redirect, request, Blueprint, jsonify
from dashmachine.settings_system.forms import ConfigForm
from dashmachine.main.utils import read_config
from dashmachine.main.models import Files
from dashmachine.paths import backgrounds_images_folder, apps_images_folder
from dashmachine.settings_system.utils import load_files_html

settings_system = Blueprint("settings_system", __name__)


@settings_system.route("/settings", methods=["GET"])
def settings():
    config_form = ConfigForm()
    with open("config.ini", "r") as config_file:
        config_form.config.data = config_file.read()
    files_html = load_files_html()
    return render_template(
        "settings_system/settings.html", config_form=config_form, files_html=files_html
    )


@settings_system.route("/settings/save_config", methods=["POST"])
def save_config():
    with open("config.ini", "w") as config_file:
        config_file.write(request.form.get("config"))
    msg = read_config()
    return jsonify(data=msg)


@settings_system.route("/settings/add_images", methods=["POST"])
def add_images():
    if request.form.get("folder") == "apps":
        dest_folder = apps_images_folder
    elif request.form.get("folder") == "backgrounds":
        dest_folder = backgrounds_images_folder
    for cached_file in request.form.get("files").split(","):
        file = Files.query.filter_by(cache=cached_file).first()
        new_path = os.path.join(dest_folder, file.name)
        os.rename(file.path, new_path)
    return load_files_html()
