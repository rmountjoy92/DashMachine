import os
import glob
from secrets import token_hex
from htmlmin.main import minify
from configparser import ConfigParser
from flask import render_template, url_for, redirect, request, Blueprint, jsonify
from flask_login import current_user
from dashmachine.main.models import Files, Apps, DataSources
from dashmachine.main.utils import (
    check_groups,
    get_data_source,
    mark_update_message_read,
)
from dashmachine.user_system.models import User
from dashmachine.settings_system.models import Settings
from dashmachine.paths import cache_folder, user_data_folder
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
    settings = Settings.query.first()
    if not check_groups(settings.home_access_groups, current_user):
        return redirect(url_for("error_pages.unauthorized"))
    return render_template("main/home.html")


@main.route("/app_view?<app_id>", methods=["GET"])
def app_view(app_id):
    settings = Settings.query.first()
    if not check_groups(settings.home_access_groups, current_user):
        return redirect(url_for("user_system.login"))
    app_db = Apps.query.filter_by(id=app_id).first()
    return render_template(
        "main/app-view.html", url=f"{app_db.prefix}{app_db.url}", title=app_db.name
    )


@main.route("/load_data_source", methods=["GET"])
def load_data_source():
    data_source = DataSources.query.filter_by(id=request.args.get("id")).first()
    data = get_data_source(data_source)
    return data


@main.route("/change_home_view_mode?<mode>%<user_id>", methods=["GET"])
def change_home_view_mode(mode, user_id):
    user = User.query.filter_by(id=user_id).first()
    config = ConfigParser()
    config.read(os.path.join(user_data_folder, "config.ini"))
    config.set(user.username, "home_view_mode", mode)
    config.write(open(os.path.join(user_data_folder, "config.ini"), "w"))
    user.home_view_mode = mode
    db.session.merge(user)
    db.session.commit()
    return redirect(url_for("main.home"))


@main.route("/update_message_read", methods=["GET"])
def update_message_read():
    mark_update_message_read()
    return "ok"


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


# @main.route("/tcdrop/addLocalFile", methods=["GET"])
# def addLocalFile():
#     f = request.args.get("file")
#     email_cache = request.args.get("email_cache")
#     ext = f.split(".")[1]
#     random_hex = token_hex(16)
#     fn = f"{random_hex}.{ext}"
#     if email_cache == "true":
#         file = Files.query.filter_by(cache=f).first()
#         orig_fn = file.name
#         old_path = os.path.join(email_cache_folder, f)
#     else:
#         old_path = os.path.join(pdf_folder, f)
#         orig_fn = f
#     path = os.path.join(cache_folder, fn)
#     copyfile(old_path, path)
#     html = render_template(
#         "main/tcdrop-file-row.html", orig_fn=orig_fn, fn=fn, id=random_hex
#     )
#     file = Files(name=orig_fn, path=path, cache=fn, folder="cache")
#     db.session.add(file)
#     db.session.commit()
#     return jsonify(data={"file": fn, "html": html})
