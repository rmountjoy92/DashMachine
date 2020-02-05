import os
from configparser import ConfigParser
from dashmachine.main.models import Apps, ApiCalls, Groups
from dashmachine.settings_system.models import Settings
from dashmachine.paths import user_data_folder
from dashmachine import db


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def read_config():
    config = ConfigParser()
    try:
        config.read(os.path.join(user_data_folder, "config.ini"))
    except Exception as e:
        return {"msg": f"Invalid Config: {e}."}

    Apps.query.delete()
    ApiCalls.query.delete()
    Settings.query.delete()
    Groups.query.delete()

    for section in config.sections():

        # Settings creation
        if section == "Settings":
            settings = Settings()
            if "theme" in config["Settings"]:
                settings.theme = config["Settings"]["theme"]
            else:
                settings.theme = "light"

            if "accent" in config["Settings"]:
                settings.accent = config["Settings"]["accent"]
            else:
                settings.accent = "orange"

            if "background" in config["Settings"]:
                settings.background = config["Settings"]["background"]
            else:
                settings.background = "None"

            if "roles" in config["Settings"]:
                settings.roles = config["Settings"]["roles"]
                if "admin" not in settings.roles:
                    settings.roles += ",admin"
                if "user" not in settings.roles:
                    settings.roles += ",user"
                if "public_user" not in settings.roles:
                    settings.roles += ",public_user"
            else:
                settings.roles = "admin,user,public_user"

            if "home_access_groups" in config["Settings"]:
                settings.home_access_groups = config["Settings"]["home_access_groups"]
            else:
                settings.home_access_groups = "admin_only"

            if "settings_access_groups" in config["Settings"]:
                settings.settings_access_groups = config["Settings"][
                    "settings_access_groups"
                ]
            else:
                settings.settings_access_groups = "admin_only"

            db.session.add(settings)
            db.session.commit()

        # Groups creation
        elif "roles" in config[section]:
            group = Groups()
            group.name = section
            group.roles = config[section]["roles"]
            db.session.add(group)
            db.session.commit()

        # API call creation
        elif "platform" in config[section]:
            api_call = ApiCalls()
            api_call.name = section
            if "resource" in config[section]:
                api_call.resource = config[section]["resource"]
            else:
                return {"msg": f"Invalid Config: {section} does not contain resource."}

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

        else:
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

            if "groups" in config[section]:
                app.groups = config[section]["groups"]
            else:
                app.groups = None

            db.session.add(app)
            db.session.commit()

    group = Groups.query.filter_by(name="admin_only").first()
    if not group:
        group = Groups()
        group.name = "admin_only"
        group.roles = "admin"
        db.session.add(group)
        db.session.commit()
    return {"msg": "success", "settings": row2dict(settings)}
