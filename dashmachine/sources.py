import os
import random
from jsmin import jsmin
from flask_login import current_user
from dashmachine import app
from dashmachine.main.models import Apps
from dashmachine.main.utils import check_groups
from dashmachine.main.forms import TagsForm
from dashmachine.settings_system.models import Settings
from dashmachine.paths import static_folder, backgrounds_images_folder
from dashmachine.cssmin import cssmin

"""This file establishes bundles of js and css sources, minifies them using jsmin and
a dashmachine module named cssmin, adds script or style tag, uses a flask
context processor to make the process functions available to every jinja template.
Load orders in bundles are respected here"""

"""You can disable minification for debug purposes here (set to True) """
debug_js = False
debug_css = False


def process_js_sources(process_bundle=None, src=None, app_global=False):
    if src:
        process_bundle = [src]

    elif app_global is True:
        process_bundle = [
            "global/dashmachine.js",
            "global/tcdrop.js",
        ]

    html = ""
    if debug_js is True:
        for source in process_bundle:
            html += f'<script src="static/js/{source}"></script>'
        return html
    for source in process_bundle:
        source_path = os.path.join(static_folder, "js", source)
        with open(source_path) as js_file:
            minified = jsmin(js_file.read(), quote_chars="'\"`")
            html += f"<script>{minified}</script>"

    return html


def process_css_sources(process_bundle=None, src=None, app_global=False):
    if src:
        process_bundle = [src]

    elif app_global is True:
        process_bundle = [
            "global/style.css",
            "global/dashmachine-theme.css",
            "global/dashmachine.css",
            "global/tcdrop.css",
        ]

    html = ""
    if debug_css is True:
        for source in process_bundle:
            html += (
                f'<link rel="stylesheet" type="text/css" '
                f'href="static/css/{source}">'
            )
        return html
    else:
        for source in process_bundle:
            source_path = os.path.join(static_folder, "css", source)
            minified = cssmin(source_path)
            html += f"<style>{minified}</style>"

    return html


@app.context_processor
def context_processor():
    apps = []
    tags = []
    apps_db = Apps.query.all()
    for app_db in apps_db:
        if not app_db.groups:
            app_db.groups = None
        if check_groups(app_db.groups, current_user):
            apps.append(app_db)
            tags += app_db.tags.split(",")

    tags_form = TagsForm()
    tags = [tag.strip() for tag in tags]
    tags = list(dict.fromkeys(tags))
    tags_form.tags.choices += [(tag, tag) for tag in tags]
    settings = Settings.query.first()
    if settings.background == "random":
        if len(os.listdir(backgrounds_images_folder)) < 1:
            settings.background = None
        else:
            settings.background = (
                f"static/images/backgrounds/"
                f"{random.choice(os.listdir(backgrounds_images_folder))}"
            )
    return dict(
        test_key="test",
        process_js_sources=process_js_sources,
        process_css_sources=process_css_sources,
        apps=apps,
        settings=settings,
        tags_form=tags_form,
    )
