import os
import json
import socket
from configparser import ConfigParser
from dashmachine.main.models import Apps, DataSources, DataSourcesArgs, Tags
from dashmachine.user_system.models import User, AccessGroups
from dashmachine.user_system.utils import (
    hash_and_cache_password,
    get_cached_password,
    clean_auth_cache,
)
from dashmachine.settings_system.models import Settings
from dashmachine.paths import user_data_folder
from dashmachine.docs_system.core_docs import data_sources_doc_dicts
from dashmachine import db


def host_ip():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return host_ip
    except Exception:
        print("Unable to get Hostname and IP")


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def validate_json_csv(json_csv):
    try:
        for json_dict in json_csv.replace("},{", "}%,%{").split("%,%"):
            json.loads(json_dict)
        return None
    except Exception as e:
        return e


config_restored_msg = (
    "<i class='material-icons-outlined' style='font-size: 2rem'>warning</i> <br>"
    + "Invalid config! <br>"
    + "CONFIG RESTORED FROM LAST WORKING STATE. <br>"
    + "PLEASE FIX THE FOLLOWING ERRORS IN YOUR CONFIG: <br>"
)


def read_config(from_backup=False):
    # GET CONFIG OBJECT
    config = ConfigParser(interpolation=None)
    try:
        if from_backup is True:
            config.read(os.path.join(user_data_folder, ".config-backup.ini"))
        else:
            config.read(os.path.join(user_data_folder, "config.ini"))
    except Exception as e:
        return {"msg": f"{config_restored_msg} Invalid Config: {e}."}

    # RESET DATABASE VALUES
    for ag in AccessGroups.query.all():
        ag.apps = []
        db.session.merge(ag)
        db.session.commit()
    for ds in DataSources.query.all():
        ds.apps = []
        db.session.merge(ds)
        db.session.commit()
    for tag in Tags.query.all():
        tag.apps = []
        db.session.merge(tag)
        db.session.commit()

    DataSources.query.delete()
    DataSourcesArgs.query.delete()
    Apps.query.delete()
    Settings.query.delete()
    AccessGroups.query.delete()
    Tags.query.delete()
    User.query.delete()

    # ADD DEFAULT ACCESS GROUPS
    if "admin_only" not in config.sections():
        config.add_section("admin_only")
        config.set("admin_only", "roles", "admin")
        config.set("admin_only", "can_access_home", "True")
        config.set("admin_only", "can_access_user_settings", "True")
        config.set("admin_only", "can_access_main_settings", "True")
        config.set("admin_only", "can_access_card_editor", "True")
        config.set("admin_only", "can_access_docs", "True")
        config.set("admin_only", "can_access_raw_config", "True")
        config.set("admin_only", "can_see_sidenav", "True")
        config.set("admin_only", "can_edit_users", "True")
        config.set("admin_only", "can_edit_images", "True")
        config.write(open(os.path.join(user_data_folder, "config.ini"), "w"))

    if "public_users" not in config.sections():
        config.add_section("public_users")
        config.set("public_users", "roles", "public_user")
        config.set("public_users", "can_access_home", "False")
        config.set("public_users", "can_access_user_settings", "False")
        config.write(open(os.path.join(user_data_folder, "config.ini"), "w"))

    for section in config.sections():
        for key, value in config[section].items():
            if len(value) == 0:
                del config[section][key]

    settings, error = create_settings(config)
    if error:
        return error

    error = create_access_groups(config)
    if error:
        return error

    error = create_users(config)
    if error:
        return error

    error = create_data_sources(config)
    if error:
        return error

    error = create_cards(config)
    if error:
        return error

    # APPLY TAG SETTINGS
    tags_settings = config["Settings"].get("tags", "None")
    if tags_settings and tags_settings != "None":
        tags_settings = tags_settings.replace("},{", "}%,%{").split("%,%")

        for tag_setting in tags_settings:
            tag_json = json.loads(tag_setting)
            tag = Tags.query.filter_by(name=tag_json.get("name", None)).first()
            if tag:
                icon = tag_json.get("icon", None)
                if icon:
                    tag.icon = icon
                sort_pos = int(tag_json.get("sort_pos", None))
                if icon:
                    tag.sort_pos = sort_pos + 1
                db.session.merge(tag)
                db.session.commit()

    # CREATE DEFAULT USER IF NEEDED
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


def create_settings(config):
    settings = Settings()
    settings.theme = config["Settings"].get("theme", "light")
    settings.accent = config["Settings"].get("accent", "orange")
    settings.background = config["Settings"].get("background", None)
    if settings.background == "none":
        settings.background = None
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

    settings.custom_app_title = config["Settings"].get(
        "custom_app_title", "DashMachine"
    )

    settings.tags_expanded = config["Settings"].get("tags_expanded", "True")

    settings.tags = config["Settings"].get("tags", None)
    error = validate_json_csv(settings.tags)
    if error:
        return (
            None,
            {
                "msg": f"{config_restored_msg} Invalid Json for settings - tags: {error}."
            },
        )

    settings.action_providers = config["Settings"].get(
        "action_providers",
        '{"name": "Google", "macro": "g", "action": "https://www.google.com/search?q={{ value }}"}',
    )
    error = validate_json_csv(settings.action_providers)
    if error:
        return (
            None,
            {
                "msg": f"{config_restored_msg} Invalid Json for settings - action_providers: {error}."
            },
        )

    db.session.add(settings)
    db.session.commit()
    return settings, None


def create_users(config):
    # LOOP CONFIG SECTIONS
    for section in config.sections():
        if "role" in config[section] and section != "Settings":
            user = User()
            user.username = section
            user.role = config[section]["role"]
            user.theme = config[section].get("theme", None)
            user.accent = config[section].get("accent", None)
            user.background = config[section].get("background", None)
            user.tags_expanded = config[section].get("tags_expanded", "False")
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
    return None


def create_access_groups(config):
    # LOOP CONFIG SECTIONS
    for section in config.sections():
        # CREATE ACCESS GROUPS
        if "roles" in config[section] and section != "Settings":
            group = AccessGroups()
            group.name = section
            group.roles = config[section].get("roles", None)
            group.can_access_home = config[section].get("can_access_home", "True")
            group.can_access_user_settings = config[section].get(
                "can_access_user_settings", "True"
            )
            group.can_access_main_settings = config[section].get(
                "can_access_main_settings", "False"
            )
            group.can_access_card_editor = config[section].get(
                "can_access_card_editor", "False"
            )
            group.can_access_raw_config = config[section].get(
                "can_access_raw_config", "False"
            )
            group.can_access_docs = config[section].get("can_access_docs", "False")
            group.can_see_sidenav = config[section].get("can_see_sidenav", "False")
            group.can_edit_users = config[section].get("can_edit_users", "False")
            group.can_edit_images = config[section].get("can_edit_images", "False")
            db.session.add(group)
            db.session.commit()
    return None


def create_data_sources(config):
    # LOOP CONFIG SECTIONS
    for section in config.sections():

        # CREATE DATA SOURCES
        if "platform" in config[section] and section != "Settings":
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
            ds_docs = data_sources_doc_dicts(platform_name=data_source.platform)
            for variable_dict in ds_docs[0]["variables"]:
                if not DataSourcesArgs.query.filter_by(
                    key=variable_dict["variable"], data_source_id=data_source.id
                ).first() and variable_dict["variable"] not in [
                    "platform",
                    "[variable_name]",
                ]:
                    arg = DataSourcesArgs()
                    arg.key = variable_dict["variable"]
                    arg.value = None
                    arg.data_source = data_source
                    db.session.add(arg)
                    db.session.commit()
    return None


def create_cards(config):
    # LOOP CONFIG SECTIONS
    for section in config.sections():
        # skip section if..
        if "platform" in config[section]:
            continue
        elif "roles" in config[section]:
            continue
        elif "role" in config[section]:
            continue
        elif "role" in config[section]:
            continue
        elif section == "Settings":
            continue
        else:
            # START CREATE APPS
            app = Apps()
            app.name = section
            app.type = config[section].get("type", "app")

            app.prefix = config[section].get("prefix", "https://")
            if app.type == "app" and not app.prefix:
                return {
                    "msg": f"{config_restored_msg} Invalid Config: {section} does not contain prefix."
                }

            app.url = config[section].get("url", "google.com")
            host_list = ["127.0.0.1", "localhost"]
            for val in host_list[:]:
                if app.url and app.url.startswith(val):
                    app.url = host_ip() + app.url.lstrip(val)
            if app.type == "app" and not app.url:
                return {
                    "msg": f"{config_restored_msg} Invalid Config: {section} does not contain url."
                }

            app.icon = config[section].get("icon", "static/images/apps/default.png")

            app.sidebar_icon = config[section].get(
                "sidebar_icon", "static/images/apps/default.png"
            )

            app.description = config[section].get("description", None)

            app.open_in = config[section].get("open_in", "this_tab")

            app.urls = config[section].get("urls", None)
            if app.urls:
                error = validate_json_csv(app.urls)
                if error:
                    return {
                        "msg": f"{config_restored_msg} Invalid Json for collection - {app.name} - urls: {error}."
                    }

            # CREATE TAGS (DURING CREATE APPS)
            if "tags" in config[section]:
                for tag in config[section]["tags"].split(","):
                    tag = tag.strip()
                    if not Tags.query.filter_by(name=tag).first():
                        tag_db = Tags(name=tag)
                        db.session.add(tag_db)
                        db.session.commit()
                        tag_db.sort_pos = tag_db.id
                        db.session.merge(tag_db)
                        db.session.commit()
                        app.tags.append(tag_db)
                    else:
                        tag_db = Tags.query.filter_by(name=tag).first()
                        app.tags.append(tag_db)
            else:
                if not Tags.query.filter_by(name="Untagged").first():
                    tag_db = Tags(name="Untagged", sort_pos=1)
                    db.session.add(tag_db)
                    db.session.commit()
                else:
                    tag_db = Tags.query.filter_by(name="Untagged").first()
                app.tags.append(tag_db)

            db.session.add(app)
            db.session.commit()

            # CHECK IF DATA SOURCE EXISTS (DURING CREATE APPS)
            if "data_sources" in config[section]:
                for config_ds in config[section]["data_sources"].split(","):
                    db_ds = DataSources.query.filter_by(name=config_ds.strip()).first()
                    if db_ds:
                        app.data_sources.append(db_ds)
                        db.session.merge(app)
                        db.session.commit()
                    else:
                        return {
                            "msg": f"{config_restored_msg} Invalid Config: {section} has a data_source variable that doesn't exist."
                        }

            # RELATE APP TO ACCESS GROUP(S)
            if "groups" in config[section]:
                for group_name in config[section]["groups"].split(","):
                    ag = AccessGroups.query.filter_by(name=group_name.strip()).first()
                    if not ag:
                        return {
                            "msg": f"{config_restored_msg} Invalid Config: {section} contains at group that is not defined."
                        }
                    ag.apps.append(app)
                    db.session.merge(ag)
                    db.session.commit()

            # RELATE APP TO 'admin_only' GROUP
            ag = AccessGroups.query.filter_by(name="admin_only").first()
            if app not in ag.apps:
                ag.apps.append(app)
                db.session.merge(ag)
                db.session.commit()

            # END CREATE APP
    return None
