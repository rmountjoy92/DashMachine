import os
from shutil import copyfile
from requests import get
from configparser import ConfigParser
from dashmachine.paths import dashmachine_folder, images_folder
from dashmachine.main.models import Apps, ApiCalls, TemplateApps
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
    ApiCalls.query.delete()
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

            # API call creation
            if "platform" in config[section]:
                api_call = ApiCalls()
                api_call.name = section
                if "resource" in config[section]:
                    api_call.resource = config[section]["resource"]
                else:
                    return {
                        "msg": f"Invalid Config: {section} does not contain resource."
                    }

                if "method" in config[section]:
                    api_call.method = config[section]["method"]
                else:
                    api_call.method = "GET"

                if "payload" in config[section]:
                    api_call.payload = config[section]["payload"]
                else:
                    api_call.payload = None

                if "authentication" in config[section]:
                    api_call.authentication = config[section]["authentication"]
                else:
                    api_call.authentication = None

                if "username" in config[section]:
                    api_call.username = config[section]["username"]
                else:
                    api_call.username = None

                if "password" in config[section]:
                    api_call.password = config[section]["password"]
                else:
                    api_call.password = None

                if "value_template" in config[section]:
                    api_call.value_template = config[section]["value_template"]
                else:
                    api_call.value_template = section

                db.session.add(api_call)
                db.session.commit()
                continue

            # App creation
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

            if "data_template" in config[section]:
                app.data_template = config[section]["data_template"]
            else:
                app.data_template = None

            db.session.add(app)
            db.session.commit()
    return {"msg": "success", "settings": row2dict(settings)}


def read_template_apps():
    config = ConfigParser()
    try:
        config.read("app_templates.ini")
    except Exception as e:
        return {"msg": f"Invalid Config: {e}."}

    TemplateApps.query.delete()

    for section in config.sections():
        template_app = TemplateApps()
        template_app.name = section
        template_app.prefix = config[section]["prefix"]
        template_app.url = config[section]["url"]
        template_app.icon = config[section]["icon"]
        if "sidebar_icon" in config[section]:
            template_app.sidebar_icon = config[section]["sidebar_icon"]
        else:
            template_app.sidebar_icon = template_app.icon
        template_app.description = config[section]["description"]
        template_app.open_in = config[section]["open_in"]
        db.session.add(template_app)
        db.session.commit()


# establishes routes decorated w/ @public_route as accessible while not signed
# in. See login and register routes for usage
def public_route(decorated_function):
    decorated_function.is_public = True
    return decorated_function


def dashmachine_init():
    read_config()
    read_template_apps()
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


def get_rest_data(template):
    while template and template.find("{{") > -1:
        start_braces = template.find("{{") + 2
        end_braces = template.find("}}")
        key = template[start_braces:end_braces]
        key_w_braces = template[start_braces - 2 : end_braces + 2]
        value = do_api_call(key)
        template = template.replace(key_w_braces, value)
    return template


def do_api_call(key):
    api_call = ApiCalls.query.filter_by(name=key).first()
    if api_call.method.upper() == "GET":
        value = get(api_call.resource)
        exec(f"{key} = {value.json()}")
        value = str(eval(api_call.value_template))
    return value
