import os
from configparser import ConfigParser
from flask import jsonify
from dashmachine.paths import user_data_folder
from dashmachine.main.read_config import read_config
from dashmachine.main.utils import make_dict_list_string, convert_form_boolean
from dashmachine.main.models import DataSources


def modify_config(form):
    form = dict(form)
    config = ConfigParser(interpolation=None)
    try:
        config.read(os.path.join(user_data_folder, "config.ini"))
    except Exception as e:
        return {"msg": f"Invalid Config: {e}."}

    ini_section = form.get("ini_section")
    ini_id = form.get("ini_id")
    prev_name = form.get("prev_name", None)
    del form["ini_section"]
    del form["ini_id"]
    del form["prev_name"]

    ds = DataSources.query.filter_by(name=ini_id).first()
    if ds and ds.platform == ini_section:
        prev_name = ds.name
        form["name"] = form["variable_name"]
        ini_section = "Data Sources"
        del form["variable_name"]

    if ini_section == "Settings":
        prev_name = "Settings"
        action_providers = []
        tags = []
        for key, value in form.items():
            if "action_providers-" in key:
                action_providers.append((key, value))
            if "tags-" in key:
                tags.append((key, value))

        dict_list_string, ini_variable, form = make_dict_list_string(
            action_providers, form
        )
        form[ini_variable] = dict_list_string
        dict_list_string, ini_variable, form = make_dict_list_string(tags, form)
        form[ini_variable] = dict_list_string
    if ini_section == "Users":
        ini_section = form["username"]
        del form["username"]

    if ini_section == "Collection":
        urls = []
        for key, value in form.items():
            if "urls-" in key:
                urls.append((key, value))
        dict_list_string, ini_variable, form = make_dict_list_string(urls, form)
        form[ini_variable] = dict_list_string

    if ini_section in [
        "App",
        "Custom Card",
        "Access Groups",
        "Collection",
    ]:
        ini_section = form["name"]
        del form["name"]

    if ini_section == form.get("platform", None):
        ini_section = form["variable_name"]
        del form["variable_name"]

    if prev_name != "None":
        config.remove_section(prev_name)

    if ini_section in config.sections():
        while ini_section in config.sections():
            ini_section = f"{ini_section}(1)"
    if ini_section not in config.sections():
        config.add_section(ini_section)

    # print(f"{ini_section}")
    for key, value in form.items():
        # print(f"{key} - {value}")
        value = convert_form_boolean(value)
        config.set(ini_section, key, value)
    config.write(open(os.path.join(user_data_folder, "config.ini"), "w"))
    msg = read_config()
    if msg["msg"] != "success":
        read_config(from_backup=True)
    return jsonify(data=msg)
