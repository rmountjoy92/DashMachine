import os
import json
import importlib
from shutil import copyfile
from PIL import Image
from markdown2 import markdown
from configparser import ConfigParser
from flask import url_for
from dashmachine.paths import (
    images_folder,
    root_folder,
    user_data_folder,
    template_apps_folder,
    custom_platforms_folder,
    platform_folder,
)
from dashmachine.main.models import Tags
from dashmachine.main.read_config import read_config
from dashmachine.user_system.models import AccessGroups
from dashmachine.docs_system.utils import build_wiki_from_wiki_folder
from dashmachine.version import version as dashmachine_version
from dashmachine import db


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


# establishes routes decorated w/ @public_route as accessible while not signed
# in. See login and register routes for usage
def public_route(decorated_function):
    decorated_function.is_public = True
    return decorated_function


def dashmachine_init():
    resize_template_app_images()
    db.create_all()
    db.session.commit()

    # create the user_data subdirectories, link them to static
    user_backgrounds_folder = os.path.join(user_data_folder, "backgrounds")
    backgrounds_folder = os.path.join(images_folder, "backgrounds")
    if not os.path.isdir(user_backgrounds_folder):
        os.mkdir(user_backgrounds_folder)
    if not os.path.isdir(backgrounds_folder):
        os.symlink(user_backgrounds_folder, backgrounds_folder)

    user_icons_folder = os.path.join(user_data_folder, "icons")
    icons_folder = os.path.join(images_folder, "icons")
    if not os.path.isdir(user_icons_folder):
        os.mkdir(user_icons_folder)
    if not os.path.isdir(icons_folder):
        os.symlink(user_icons_folder, icons_folder)

    config_file = os.path.join(user_data_folder, "config.ini")
    if not os.path.exists(config_file):
        copyfile("default_config.ini", config_file)

    read_config()

    # delete broken links in platforms
    for file in os.listdir(platform_folder):
        path = os.path.join(platform_folder, file)
        if os.path.islink(path) and not os.path.exists(os.readlink(path)):
            os.unlink(path)

    # link platforms in user_data/platforms
    if os.path.isdir(custom_platforms_folder):
        for file in os.listdir(custom_platforms_folder):
            real_path = os.path.join(custom_platforms_folder, file)
            link_path = os.path.join(platform_folder, f"custom_{file}")
            if not os.path.exists(link_path):
                os.symlink(real_path, link_path)

    # run on_startup platform methods
    for platform_file in os.listdir(platform_folder):
        name, extension = os.path.splitext(platform_file)
        if extension.lower() == ".py" and name not in ["__init__"]:
            module = importlib.import_module(f"dashmachine.platform.{name}", ".")
            platform = module.Platform()
            if getattr(platform, "on_startup", None):
                platform.on_startup()

    # build wiki
    build_wiki_from_wiki_folder()


def get_access_group(user, page=None):
    access_groups = []
    access_group = None
    if user.is_authenticated:
        access_group = AccessGroups()

        for ag in AccessGroups.query.all():
            if user.role in ag.roles:
                access_groups.append(ag)
        for ag in access_groups:
            for app in ag.apps:
                access_group.apps.append(app)
            for key, value in row2dict(ag).items():
                if key.startswith("can_") and value == "True":
                    setattr(access_group, key, value)

    if not access_group:
        access_group = AccessGroups.query.filter_by(name="public_users").first()

    redirect_url = url_for("error_pages.unauthorized")
    if page == "home" and access_group.can_access_home == "False":
        pass
    elif page == "docs" and access_group.can_access_docs == "False":
        pass
    else:
        redirect_url = None

    return access_group, redirect_url


def get_apps_and_tags(access_group):
    apps = access_group.apps
    tags = Tags.query.order_by(Tags.sort_pos).all()

    for app in apps:
        if app.urls:
            url_list = app.urls.replace("},{", "}%,%{").split("%,%")
            app.urls_json = []
            for url in url_list:
                app.urls_json.append(json.loads(url))
    return apps, tags


def get_data_source(data_source):
    data_source_args = {}
    for arg in data_source.args:
        arg = row2dict(arg)
        if arg["value"] != "None":
            data_source_args[arg.get("key")] = arg.get("value")
    data_source = row2dict(data_source)
    module = importlib.import_module(
        f"dashmachine.platform.{data_source['platform']}", "."
    )
    platform = module.Platform(data_source, **data_source_args)
    return platform.process()


def resize_template_app_images():
    folder = os.path.join(images_folder, "apps")
    for file in os.listdir(folder):
        fp = os.path.join(folder, file)
        image = Image.open(fp)
        image.thumbnail((64, 64))
        image.save(fp)


def get_template_apps():
    app_templates = []
    for file in os.listdir(template_apps_folder):
        config = ConfigParser(interpolation=None)
        config.read(os.path.join(template_apps_folder, file))
        app_templates.append(
            {
                "name": config.sections()[0],
                "prefix": config[config.sections()[0]]["prefix"],
                "url": config[config.sections()[0]]["url"],
                "icon": config[config.sections()[0]]["icon"],
                "sidebar_icon": config[config.sections()[0]]["sidebar_icon"],
                "description": config[config.sections()[0]]["description"],
                "open_in": config[config.sections()[0]]["open_in"],
            }
        )
    return app_templates


def get_update_message_html():
    try:
        with open(os.path.join(user_data_folder, ".has_read_update"), "r") as has_read:
            has_read_version = has_read.read()
    except FileNotFoundError:
        has_read_version = None
    if not has_read_version or has_read_version.strip() != dashmachine_version:
        with open(
            os.path.join(root_folder, "update_message.md"), "r"
        ) as update_message:
            md = update_message.read()

        config_html = markdown(
            md,
            extras=[
                "tables",
                "fenced-code-blocks",
                "break-on-newline",
                "header-ids",
                "code-friendly",
            ],
        )
        return config_html
    else:
        return ""


def mark_update_message_read():
    with open(os.path.join(user_data_folder, ".has_read_update"), "w") as has_read:
        has_read.write(dashmachine_version)


def convert_form_boolean(value):
    if value == "on":
        return_value = "True"
    elif value == "off":
        return_value = "False"
    else:
        return_value = value
    return return_value


def make_dict_list_string(tuple_list, form):
    dict_list = []
    form_ids = []
    for subvariable_tuple in tuple_list:
        del form[subvariable_tuple[0]]
        ini_variable = subvariable_tuple[0].split("-")[0]
        form_ids.append(subvariable_tuple[0].split("-")[2])

    for form_id in set(form_ids):
        subvariable_dict = {}
        for subvariable_tuple in tuple_list:
            if form_id in subvariable_tuple[0]:
                st_val = convert_form_boolean(subvariable_tuple[1])
                subvariable_dict[subvariable_tuple[0].split("-")[1]] = st_val
        dict_list.append(json.dumps(subvariable_dict))

    dict_list_string = ",".join(map(str, dict_list))
    return dict_list_string, ini_variable, form


def backup_working_config():
    with open(os.path.join(user_data_folder, "config.ini"), "r") as config_file:
        with open(
            os.path.join(user_data_folder, ".config-backup.ini"), "w"
        ) as bak_file:
            bak_file.write(config_file.read())
