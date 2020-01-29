import os
from shutil import copyfile
from configparser import ConfigParser

from dashmachine.paths import dashmachine_folder, images_folder
from dashmachine.main.models import Apps
from dashmachine.settings_system.models import Settings
from dashmachine.user_system.models import User
from dashmachine.user_system.utils import add_edit_user
from dashmachine import db


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def read_config():
    config = ConfigParser()
    try:
        config.read("dashmachine/user_data/config.ini")
    except Exception as e:
        return {"msg": f"Invalid Config: {e}."}

    Apps.query.delete()
    Settings.query.delete()

    try:
        settings = Settings(
            theme=config["Settings"]["theme"],
            accent=config["Settings"]["accent"],
            background=config["Settings"]["background"],
        )
        db.session.add(settings)
        db.session.commit()
    except Exception as e:
        return {"msg": f"Invalid Config: {e}."}

    for section in config.sections():
        if section != "Settings":
            app = Apps()
            app.name = section
            if "prefix" in config[section]:
                app.prefix = config[section]["prefix"]
            else:
                return {"msg": f"Invalid Config: {section} does not contain prefix."}

            if "url" in config[section]:
                app.url = config[section]["url"]
            else:
                return {"msg": f"Invalid Config: {section} does not contain url."}

            if "icon" in config[section]:
                app.icon = config[section]["icon"]
            else:
                app.icon = None

            if "sidebar_icon" in config[section]:
                app.sidebar_icon = config[section]["sidebar_icon"]
            else:
                app.sidebar_icon = app.icon

            if "description" in config[section]:
                app.description = config[section]["description"]
            else:
                app.description = None

            if "open_in" in config[section]:
                app.open_in = config[section]["open_in"]
            else:
                app.open_in = "this_tab"

            db.session.add(app)
            db.session.commit()
    return {"msg": "success", "settings": row2dict(settings)}


# establishes routes decorated w/ @public_route as accessible while not signed
# in. See login and register routes for usage
def public_route(decorated_function):
    decorated_function.is_public = True
    return decorated_function


def dashmachine_init():
    user_data_folder = os.path.join(dashmachine_folder, "user_data")

    # create the user_data subdirectories, link them to static
    user_backgrounds_folder = os.path.join(user_data_folder, "backgrounds")
    if not os.path.isdir(user_backgrounds_folder):
        os.mkdir(user_backgrounds_folder)
        os.symlink(user_backgrounds_folder, os.path.join(images_folder, "backgrounds"))

    icons_folder = os.path.join(user_data_folder, "icons")
    if not os.path.isdir(icons_folder):
        os.mkdir(icons_folder)
        os.symlink(icons_folder, os.path.join(images_folder, "icons"))

    config_file = os.path.join(user_data_folder, "config.ini")
    if not os.path.exists(config_file):
        copyfile("default_config.ini", config_file)
        read_config()

    user = User.query.first()
    if not user:
        add_edit_user(username="admin", password="admin")