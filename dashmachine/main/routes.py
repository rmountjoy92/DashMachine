import os
import glob
from secrets import token_hex
from htmlmin.main import minify
from flask import render_template, url_for, redirect, request, Blueprint, jsonify
from flask_login import current_user
from dashmachine.main.models import Files
from dashmachine.main.utils import get_rest_data
from dashmachine.paths import cache_folder
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


# blocks access to all pages (except public routes) unless the user is
# signed in.
@main.before_app_request
def check_valid_login():

    if any(
        [
            request.endpoint.startswith("static"),
            current_user.is_authenticated,
            getattr(app.view_functions[request.endpoint], "is_public", False),
        ]
    ):
        return

    else:
        return redirect(url_for("user_system.login"))


# ------------------------------------------------------------------------------
# /home
# ------------------------------------------------------------------------------
@main.route("/")
@main.route("/home", methods=["GET", "POST"])
def home():
    return render_template("main/home.html")


@main.route("/app_view?<url>", methods=["GET"])
def app_view(url):
    return render_template("main/app-view.html", url=f"https://{url}")


@main.route("/load_rest_data", methods=["GET"])
def load_rest_data():
    data_template = get_rest_data(request.args.get("template"))
    return data_template[:50]


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
