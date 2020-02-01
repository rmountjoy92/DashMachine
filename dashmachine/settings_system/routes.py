import os
from flask import render_template, request, Blueprint, jsonify
from dashmachine.settings_system.forms import ConfigForm
from dashmachine.user_system.forms import UserForm
from dashmachine.user_system.utils import add_edit_user
from dashmachine.main.utils import read_config, row2dict
from dashmachine.main.models import Files, TemplateApps
from dashmachine.paths import backgrounds_images_folder, icons_images_folder
from dashmachine.update import check_needed, update_dashmachine
from dashmachine.version import version
from dashmachine.settings_system.utils import load_files_html

settings_system = Blueprint("settings_system", __name__)


@settings_system.route("/settings", methods=["GET"])
def settings():
    config_form = ConfigForm()
    user_form = UserForm()
    with open("dashmachine/user_data/config.ini", "r") as config_file:
        config_form.config.data = config_file.read()
    files_html = load_files_html()
    template_apps = []
    t_apps = TemplateApps.query.all()
    for t_app in t_apps:
        template_apps.append(f"{t_app.name}&&{t_app.icon}")
    return render_template(
        "settings_system/settings.html",
        config_form=config_form,
        files_html=files_html,
        user_form=user_form,
        template_apps=",".join(template_apps),
        version=version,
    )


@settings_system.route("/settings/save_config", methods=["POST"])
def save_config():
    with open("dashmachine/user_data/config.ini", "w") as config_file:
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
        os.rename(file.path, new_path)
    return load_files_html()


@settings_system.route("/settings/get_app_template", methods=["GET"])
def get_app_template():
    template_app = TemplateApps.query.filter_by(name=request.args.get("name")).first()
    template = f"[{template_app.name}]<br>"
    for key, value in row2dict(template_app).items():
        if key not in ["id", "name"]:
            template += f"{key} = {value}<br>"
    return template


@settings_system.route("/settings/update", methods=["GET"])
def update():
    update_dashmachine()
    return "ok"


@settings_system.route("/settings/check_update", methods=["GET"])
def check_update():
    return str(check_needed())


@settings_system.route("/settings/edit_user", methods=["POST"])
def edit_user():
    form = UserForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            return jsonify(data={"err": "Passwords don't match"})
        add_edit_user(form.username.data, form.password.data)
    else:
        err_str = ""
        for fieldName, errorMessages in form.errors.items():
            err_str += f"{fieldName}: "
            for err in errorMessages:
                err_str += f"{err} "
        return jsonify(data={"err": err_str})
    return jsonify(data={"err": "success"})
