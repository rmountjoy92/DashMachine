from configparser import ConfigParser
from dashmachine.main.models import Apps
from dashmachine.settings_system.models import Settings
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
