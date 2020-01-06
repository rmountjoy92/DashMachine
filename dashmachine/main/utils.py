from configparser import ConfigParser, DuplicateSectionError
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
        config.read("config.ini")
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
            try:
                app = Apps(
                    name=section,
                    prefix=config[section]["prefix"],
                    url=config[section]["url"],
                    icon=config[section]["icon"],
                    sidebar_icon=config[section]["sidebar_icon"],
                    description=config[section]["description"],
                    open_in=config[section]["open_in"],
                )
                db.session.add(app)
                db.session.commit()
            except KeyError as e:
                return {"msg": f"Invalid Config: {section} does not contain {e}."}
    return {"msg": "success", "settings": row2dict(settings)}


# establishes routes decorated w/ @public_route as accessible while not signed
# in. See login and register routes for usage
def public_route(decorated_function):
    decorated_function.is_public = True
    return decorated_function
