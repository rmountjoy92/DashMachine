import os
import glob
import json
from secrets import token_hex
from htmlmin.main import minify
from flask import (
    render_template,
    url_for,
    redirect,
    request,
    Blueprint,
    jsonify,
    render_template_string,
)
from flask_login import current_user
from dashmachine.main.models import Files, Apps, DataSources
from dashmachine.main.utils import (
    get_data_source,
    mark_update_message_read,
    row2dict,
    get_apps_and_tags,
    get_access_group,
    backup_working_config,
    get_template_apps,
)
from dashmachine.main.modify_config import modify_config
from dashmachine.settings_system.models import Settings
from dashmachine.settings_system.forms import ConfigForm
from dashmachine.settings_system.utils import load_files_html
from dashmachine.docs_system.utils import get_card_doc_dict
from dashmachine.docs_system.core_docs import (
    configured_data_sources_doc_dicts,
    settings_doc_dict,
    user_settings_doc_dict,
    access_groups_doc_dict,
    data_sources_doc_dicts,
)
from dashmachine.user_system.models import User, AccessGroups
from dashmachine.paths import cache_folder, user_data_folder
from dashmachine.version import version, revision_number
from dashmachine import app, db


main = Blueprint("main", __name__)


# ------------------------------------------------------------------------------
# intial routes and functions (before/after request)
# ------------------------------------------------------------------------------
@app.after_request
def response_minify(response):
    """
    minify html response to decrease site traffic
    """
    if response.content_type == "text/html; charset=utf-8":
        response.set_data(minify(response.get_data(as_text=True)))

        return response
    return response


# ------------------------------------------------------------------------------
# /home
# ------------------------------------------------------------------------------
@main.route("/")
@main.route("/home", methods=["GET"])
def home():
    access_group, redirect_url = get_access_group(current_user, page="home")
    if redirect_url:
        return redirect(redirect_url)
    apps, tags = get_apps_and_tags(access_group)
    return render_template(
        "main/home.html", apps=apps, tags=tags, access_group=access_group, page="home"
    )


# ------------------------------------------------------------------------------
# /home modules
# ------------------------------------------------------------------------------
@main.route("/load_apps", methods=["GET"])
def load_apps():
    access_group, redirect_url = get_access_group(current_user)
    apps, tags = get_apps_and_tags(access_group)

    if request.args.get("home", None) == "true":
        html = render_template_string(
            """
            {% from 'main/cards.html' import HomeCards %}
            {{ HomeCards(apps, tags) }}
            """,
            apps=apps,
            tags=tags,
        )
    elif request.args.get("sidenav", None) == "true":
        html = render_template_string(
            """
            {% from 'main/cards.html' import SidenavApps %}
            {{ SidenavApps(apps, tags) }}
            """,
            apps=apps,
            tags=tags,
        )
    return html


@main.route("/load_card_editor", methods=["GET"])
def load_card_editor():
    access_group, redirect_url = get_access_group(current_user)
    apps, tags = get_apps_and_tags(access_group)
    data_sources = []
    for ds in DataSources.query.all():
        data_sources.append({"id": ds.id, "name": ds.name, "platform": ds.platform})
    card_editor_html = render_template_string(
        """
        {% from 'main/card-editor.html' import CardEditor with context %}
        {{ CardEditor() }}
        """,
        data_sources=data_sources,
        apps=apps,
    )
    return card_editor_html


@main.route("/load_config_editor", methods=["GET"])
def load_config_editor():
    config_form = ConfigForm()
    with open(os.path.join(user_data_folder, "config.ini"), "r") as config_file:
        config_form.config.data = config_file.read()
    config_editor_html = render_template_string(
        """
        {% from 'main/config-editor.html' import ConfigEditor with context %}
        {{ ConfigEditor() }}
        """,
        config_form=config_form,
    )
    return config_editor_html


@main.route("/load_settings_editor", methods=["GET"])
def load_settings_editor():
    settings_db = Settings.query.first()
    files_html = load_files_html()
    access_group, redirect_url = get_access_group(current_user)

    access_groups = AccessGroups.query.all()
    users = User.query.all()

    # GUI DICTS
    user_dicts = [row2dict(user) for user in User.query.all()]
    for user_dict in user_dicts:
        user_dict["password"] = None
    user_settings_doc_dict["docs_url"] = url_for(
        "docs_system.docs_main_settings", _anchor="user-settings"
    )
    settings_dict = row2dict(settings_db)
    settings_doc_dict["docs_url"] = url_for("docs_system.docs_main_settings")
    settings_dict["action_providers"] = ["list"] + [
        json.loads(tag_json)
        for tag_json in settings_dict["action_providers"]
        .replace("},{", "}%,%{")
        .split("%,%")
    ]
    if settings_dict.get("tags", "None") != "None":
        settings_dict["tags"] = ["list"] + [
            json.loads(tag_json)
            for tag_json in settings_dict["tags"].replace("},{", "}%,%{").split("%,%")
        ]
    settings_editor_html = render_template_string(
        """
        {% from 'main/settings-editor.html' import SettingsEditor with context %}
        {{ SettingsEditor() }}
        """,
        files_html=files_html,
        version=version,
        revision_number=revision_number,
        user_dicts=user_dicts,
        settings_dict=settings_dict,
        settings_doc_dict=settings_doc_dict,
        user_settings_doc_dict=user_settings_doc_dict,
        access_group=access_group,
        access_groups=access_groups,
        users=users,
    )
    backup_working_config()
    return settings_editor_html


@main.route("/app_view?<app_id>", methods=["GET"])
def app_view(app_id):
    access_group, redirect_url = get_access_group(current_user)
    apps, tags = get_apps_and_tags(access_group)
    if redirect_url:
        return redirect(redirect_url)
    app_db = Apps.query.filter_by(id=app_id).first()
    return render_template(
        "main/app-view.html",
        url=f"{app_db.prefix}{app_db.url}",
        title=app_db.name,
        access_group=access_group,
        apps=apps,
        tags=tags,
    )


@main.route("/load_data_source", methods=["GET"])
def load_data_source():
    data_source = DataSources.query.filter_by(id=request.args.get("id")).first()
    data = get_data_source(data_source)
    return data


@main.route("/update_message_read", methods=["GET"])
def update_message_read():
    mark_update_message_read()
    return "ok"


@main.route("/build_action_provider_url", methods=["GET"])
def build_action_provider_url():
    url = render_template_string(
        request.args.get("action"), value=request.args.get("value")
    )
    return url


@main.route("/get_card_editor_form", methods=["GET"])
def get_card_editor_form():
    app_templates = None
    if request.args.get("type", None) == "app":
        new_app = Apps(type="app")
        card = row2dict(new_app)
        app_templates = get_template_apps()

    elif request.args.get("type", None) == "collection":
        new_app = Apps(type="collection")
        card = row2dict(new_app)
        card["urls"] = '{"url": "", "icon": "", "name": "", "open_in": ""}'
    elif request.args.get("type", None) == "custom":
        new_app = Apps(type="custom")
        card = row2dict(new_app)
    else:
        card_db = Apps.query.filter_by(id=request.args.get("app_id")).first()
        card = row2dict(card_db)
        card["tags"] = ",".join([tag.name for tag in card_db.tags])
        card["groups"] = ",".join([group.name for group in card_db.access_groups])
        card["data_sources"] = ",".join([ds.name for ds in card_db.data_sources])

    if not card.get("tags", None):
        card["tags"] = ""
    if not card.get("groups", None):
        card["groups"] = ""
    if not card.get("data_sources", None):
        card["data_sources"] = ""

    if card["urls"] != "None":
        urls = card["urls"]
        del card["urls"]
        card["urls"] = ["list"] + [
            json.loads(url_json)
            for url_json in urls.replace("},{", "}%,%{").split("%,%")
        ]
    doc_dict = get_card_doc_dict(card["type"])
    if card["type"] == "app":
        anchor = "cards-apps"
    elif card["type"] == "collection":
        anchor = "cards-collection"
    elif card["type"] == "custom":
        anchor = "cards-custom"
    doc_dict["docs_url"] = url_for("docs_system.docs_cards", _anchor=anchor)
    form_html = render_template_string(
        """
        {% from 'main/ini-form.html' import INIForm %}
        {% if card['name'] != 'None' %}
            <h5 class="theme-primary-text">Editing {{ card['name'] }}</h5>
        {% else %}
            <h5 class="theme-primary-text">New {{ doc_dict['name'] }}</h5>
        {% endif %}
        {{ INIForm(card, doc_dict, location="card-editor", app_templates=app_templates) }}
        """,
        card=card,
        doc_dict=doc_dict,
        app_templates=app_templates,
    )
    return form_html


@main.route("/get_card_editor_ds_form", methods=["GET"])
def get_card_editor_ds_form():
    ds_selector = None

    if request.args.get("new", None) == "True":
        data_source = {}
        doc_dict = {}
        ds_selector = [ds["name"] for ds in data_sources_doc_dicts(get_all=True)]
    elif request.args.get("platform", None):
        doc_dict = data_sources_doc_dicts(platform_name=request.args.get("platform"))[0]
        for variable in doc_dict["variables"]:
            if variable["variable"] == "platform":
                variable["disabled"] = "True"
        data_source = {
            "name": "",
            "variable_name": "",
            "platform": doc_dict["name"],
        }
        for arg in doc_dict["variables"]:
            if arg["variable"] != "platform":
                data_source[arg["variable"]] = ""

    else:
        ds = DataSources.query.filter_by(id=request.args.get("ds_id")).first()
        data_source = {
            "id": ds.id,
            "name": ds.name,
            "variable_name": ds.name,
            "platform": ds.platform,
        }
        for arg in ds.args:
            data_source[arg.key] = arg.value

        doc_dict = configured_data_sources_doc_dicts(data_source["id"])
        doc_dict["docs_url"] = url_for(
            "docs_system.docs_data_sources", _anchor=ds.platform
        )
    form_html = render_template_string(
        """
        {% from 'main/ini-form.html' import INIForm %}
        {% if not ds_selector %}
            {% if data_source['name']|length > 0 %}
                <h5 class="theme-primary-text">Editing {{ data_source['name'] }}</h5>
            {% else %}
                <h5 class="theme-primary-text">New {{ doc_dict['name'] }}</h5>
            {% endif %}
        {% endif %}
        {{ INIForm(ini_dict=data_source, doc_dict=doc_dict, ds_selector=ds_selector) }}
        """,
        data_source=data_source,
        doc_dict=doc_dict,
        ds_selector=ds_selector,
    )
    return form_html


@main.route("/get_settings_editor_ag_form", methods=["GET"])
def get_settings_editor_ag_form():
    if request.args.get("new", None) == "True":
        ag = AccessGroups()
        ag = row2dict(ag)
        for key, value in ag.items():
            if "can_" in key:
                ag[key] = "False"
        new = True
    else:
        ag = AccessGroups.query.filter_by(id=request.args.get("ag_id")).first()
        ag = row2dict(ag)
        new = False
    form_html = render_template_string(
        """
        {% from 'main/ini-form.html' import INIForm %}
        {% if new %}
            <h5 class="theme-primary-text">New Access Group</h5>
        {% else %}
            <h5 class="theme-primary-text">Editing {{ ag['name'] }}</h5>
        {% endif %}
        {{ INIForm(ag, doc_dict) }}
        """,
        ag=ag,
        doc_dict=access_groups_doc_dict,
        new=new,
    )
    return form_html


@main.route("/get_settings_editor_user_form", methods=["GET"])
def get_settings_editor_user_form():
    if request.args.get("new", None) == "True":
        user = row2dict(User())
        new = True
    else:
        user = row2dict(User.query.filter_by(id=request.args.get("user_id")).first())
        user["password"] = None
        new = False

    user["name"] = user["username"]
    user_settings_doc_dict["docs_url"] = url_for(
        "docs_system.docs_main_settings", _anchor="user-settings"
    )
    form_html = render_template_string(
        """
        {% from 'main/ini-form.html' import INIForm %}
        {% if new %}
            <h5 class="theme-primary-text">New User</h5>
        {% else %}
            <h5 class="theme-primary-text">Editing {{ user['username'] }}</h5>
        {% endif %}
        {{ INIForm(user, user_settings_doc_dict, location="settings-editor") }}
        """,
        user=user,
        user_settings_doc_dict=user_settings_doc_dict,
        new=new,
    )
    return form_html


@main.route("/save_ini_form_to_config", methods=["POST"])
def save_ini_form_to_config():
    # for key, value in request.form.items():
    #     print(f"{key} - {value}")
    # return "ok"
    return modify_config(request.form)


# ------------------------------------------------------------------------------
# TCDROP routes
# ------------------------------------------------------------------------------
@main.route("/tcdrop/cacheFile", methods=["POST"])
def cacheFile():
    f = request.files.get("file")
    ext = f.filename.split(".")[1]
    random_hex = token_hex(16)
    fn = f"{random_hex}.{ext}"
    path = os.path.join(cache_folder, fn)
    f.save(path)
    html = render_template(
        "main/tcdrop-file-row.html", orig_fn=f.filename, fn=fn, id=random_hex
    )
    file = Files(name=f.filename, path=path, cache=fn, folder="cache")
    db.session.add(file)
    db.session.commit()
    return jsonify(data={"cached": fn, "html": html})


@main.route("/tcdrop/clearCache", methods=["GET"])
def clearCache():
    files = glob.glob(cache_folder + "/*")
    for file in files:
        if ".no" not in file:
            os.remove(file)
    Files.query.filter_by(folder="cache").delete()
    db.session.commit()
    return "success"


@main.route("/tcdrop/deleteCachedFile", methods=["GET"])
def deleteCachedFile():
    f = request.args.get("file")
    path = os.path.join(cache_folder, f)
    Files.query.filter_by(path=path).delete()
    db.session.commit()
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    return "success"
