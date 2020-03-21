import os
from configparser import ConfigParser
from dashmachine.main.models import Apps, Groups, DataSources, DataSourcesArgs, Tags
from dashmachine.user_system.models import User
from dashmachine.user_system.utils import (
    hash_and_cache_password,
    get_cached_password,
    clean_auth_cache,
)
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

    ds_list = DataSources.query.all()
    for ds in ds_list:
        ds.apps.clear()
    DataSources.query.delete()
    DataSourcesArgs.query.delete()
    Apps.query.delete()
    Settings.query.delete()
    Groups.query.delete()
    Tags.query.delete()
    User.query.delete()

    for section in config.sections():

        # Settings creation
        if section == "Settings":
            settings = Settings()

            settings.theme = config["Settings"].get("theme", "light")

            settings.accent = config["Settings"].get("accent", "orange")

            settings.background = config["Settings"].get("background", "None")

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

            settings.home_access_groups = config["Settings"].get(
                "home_access_groups", "admin_only"
            )

            settings.settings_access_groups = config["Settings"].get(
                "settings_access_groups", "admin_only"
            )
            settings.home_view_mode = config["Settings"].get("home_view_mode", "grid")

            settings.custom_app_title = config["Settings"].get(
                "custom_app_title", "DashMachine"
            )

            settings.sidebar_default = config["Settings"].get("sidebar_default", "open")

            db.session.add(settings)
            db.session.commit()

        # User creation
        elif "role" in config[section]:
            user = User()
            user.username = section
            user.role = config[section]["role"]
            user.sidebar_default = config[section].get("sidebar_default", None)
            user.home_view_mode = config[section].get("home_view_mode", "grid")
            user.theme = config[section].get("theme", None)
            user.accent = config[section].get("accent", None)
            user.password = ""
            if not User.query.filter_by(role="admin").first() and user.role != "admin":
                print(
                    f"Invalid Config: admin user not specified, or not specified first. {user.username} role set to admin"
                )
                user.role = "admin"
                config.set(section, "role", "admin")
                config.write(open(os.path.join(user_data_folder, "config.ini"), "w"))
            db.session.add(user)
            db.session.commit()
            new_password = config[section].get("password", None)
            if new_password:
                if new_password == config[section].get("confirm_password", None):
                    password = hash_and_cache_password(new_password, user.id)
                    user.password = password
                    db.session.merge(user)
                    db.session.commit()
            else:
                password = get_cached_password(user.id)
                if password == "error":
                    print(
                        f"Invalid Config: Password for {user.username} must be specified. Using 'admin' by default"
                    )
                user.password = password
                db.session.merge(user)
                db.session.commit()
            config.set(section, "password", "")
            config.set(section, "confirm_password", "")
            config.write(open(os.path.join(user_data_folder, "config.ini"), "w"))

        # Groups creation
        elif "roles" in config[section]:
            group = Groups()
            group.name = section
            group.roles = config[section]["roles"]
            db.session.add(group)
            db.session.commit()

        # Data source creation
        elif "platform" in config[section]:
            data_source = DataSources()
            data_source.name = section
            data_source.platform = config[section]["platform"]
            db.session.add(data_source)
            db.session.commit()
            for key, value in config[section].items():
                if key not in ["name", "platform"]:
                    arg = DataSourcesArgs()
                    arg.key = key
                    arg.value = value
                    arg.data_source = data_source
                    db.session.add(arg)
                    db.session.commit()

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

            if "groups" in config[section]:
                for group_name in config[section]["groups"].split(","):
                    if not Groups.query.filter_by(name=group_name.strip()).first():
                        return {
                            "msg": f"Invalid Config: {section} contains at group that is not defined."
                        }
                app.groups = config[section]["groups"]
            else:
                app.groups = None

            if "tags" in config[section]:
                app.tags = config[section]["tags"].title()
                for tag in app.tags.split(","):
                    tag = tag.strip().title()
                    if not Tags.query.filter_by(name=tag).first():
                        tag_db = Tags(name=tag)
                        db.session.add(tag_db)
                        db.session.commit()
            else:
                if Tags.query.first():
                    app.tags = "Untagged"
                    if not Tags.query.filter_by(name="Untagged").first():
                        tag_db = Tags(name="Untagged")
                        db.session.add(tag_db)
                        db.session.commit()
                else:
                    app.tags = None

            db.session.add(app)
            db.session.commit()

            if "data_sources" in config[section]:
                for config_ds in config[section]["data_sources"].split(","):
                    db_ds = DataSources.query.filter_by(name=config_ds.strip()).first()
                    if db_ds:
                        app.data_sources.append(db_ds)
                        db.session.merge(app)
                        db.session.commit()
                    else:
                        return {
                            "msg": f"Invalid Config: {section} has a data_source variable that doesn't exist."
                        }

    group = Groups.query.filter_by(name="admin_only").first()
    if not group:
        group = Groups()
        group.name = "admin_only"
        group.roles = "admin"
        db.session.add(group)
        db.session.commit()

    clean_auth_cache()
    if not User.query.first():
        user = User()
        user.username = "admin"
        user.role = "admin"
        user.password = ""
        db.session.add(user)
        db.session.commit()
        user.password = hash_and_cache_password("admin", user.id)
        db.session.merge(user)
        db.session.commit()
    return {"msg": "success", "settings": row2dict(settings)}
