import os
import importlib
from shutil import copyfile
from PIL import Image
from dashmachine.paths import dashmachine_folder, images_folder
from dashmachine.main.models import Groups
from dashmachine.main.read_config import read_config
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

    user_data_folder = os.path.join(dashmachine_folder, "user_data")

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


def check_groups(groups, current_user):
    if current_user.is_anonymous:
        current_user.role = "public_user"

    if groups:
        groups_list = groups.split(",")
        roles_list = []
        for group in groups_list:
            group = Groups.query.filter_by(name=group.strip()).first()
            for group_role in group.roles.split(","):
                roles_list.append(group_role.strip())
        if current_user.role in roles_list:
            return True
        else:
            return False
    else:
        if current_user.role == "admin":
            return True
        else:
            return False


def get_data_source(data_source):
    data_source_args = {}
    for arg in data_source.args:
        arg = row2dict(arg)
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
