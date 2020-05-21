import os
from flask import render_template, Blueprint, redirect, request
from flask_login import current_user
from dashmachine.paths import root_folder, wiki_folder
from dashmachine.docs_system.core_docs import (
    settings_doc_dict,
    user_settings_doc_dict,
    apps_doc_dict,
    collections_doc_dict,
    custom_card_doc_dict,
    data_sources_doc_dicts,
    access_groups_doc_dict,
)
from dashmachine.docs_system.utils import (
    get_md_from_file,
    get_md_from_dict,
    get_toc_md_from_dicts,
    create_edit_wiki,
)
from dashmachine.moment import create_moment
from dashmachine.main.utils import get_apps_and_tags, get_access_group
from dashmachine.main.models import Wiki, WikiTags

docs_system = Blueprint("docs_system", __name__)


@docs_system.route("/docs_home", methods=["GET"])
def docs_home():
    access_group, redirect_url = get_access_group(current_user, page="docs")
    apps, tags = get_apps_and_tags(access_group)
    if redirect_url:
        return redirect(redirect_url)
    return render_template(
        "docs_system/docs-home.html",
        about_html=get_md_from_file(os.path.join(root_folder, "README.md")),
        install_html=get_md_from_file("install.md"),
        getting_started_html=get_md_from_file("getting-started.md"),
        access_group=access_group,
        apps=apps,
        tags=tags,
    )


@docs_system.route("/docs_main_settings", methods=["GET"])
def docs_main_settings():
    access_group, redirect_url = get_access_group(current_user, page="docs")
    if redirect_url:
        return redirect(redirect_url)
    apps, tags = get_apps_and_tags(access_group)
    return render_template(
        "docs_system/docs-main-settings.html",
        main_settings_html=get_md_from_dict(settings_doc_dict),
        user_settings_html=get_md_from_dict(user_settings_doc_dict),
        ag_settings_html=get_md_from_dict(access_groups_doc_dict),
        access_group=access_group,
        apps=apps,
        tags=tags,
    )


@docs_system.route("/docs_cards", methods=["GET"])
def docs_cards():
    access_group, redirect_url = get_access_group(current_user, page="docs")
    if redirect_url:
        return redirect(redirect_url)
    apps, tags = get_apps_and_tags(access_group)
    return render_template(
        "docs_system/docs-cards.html",
        apps_html=get_md_from_dict(apps_doc_dict),
        collections_html=get_md_from_dict(collections_doc_dict),
        custom_cards_html=get_md_from_dict(custom_card_doc_dict),
        access_group=access_group,
        apps=apps,
        tags=tags,
    )


@docs_system.route("/docs_data_sources", methods=["GET"])
def docs_data_sources():
    access_group, redirect_url = get_access_group(current_user, page="docs")
    if redirect_url:
        return redirect(redirect_url)
    apps, tags = get_apps_and_tags(access_group)
    doc_dicts = data_sources_doc_dicts(get_all=True)
    data_sources_html = get_toc_md_from_dicts(doc_dicts)
    for doc in doc_dicts:
        data_sources_html += f"\n\n{get_md_from_dict(doc)}"
    return render_template(
        "docs_system/docs-data-sources.html",
        data_sources_main_html=get_md_from_file("data-sources.md"),
        creating_platforms_html=get_md_from_file("creating-platforms.md"),
        platform_methods_html=get_md_from_file("platform-methods.md"),
        data_sources_html=data_sources_html,
        access_group=access_group,
        apps=apps,
        tags=tags,
    )


@docs_system.route("/wiki_tags", methods=["GET"])
def wiki_tags():
    access_group, redirect_url = get_access_group(current_user, page="wikis")
    if redirect_url:
        return redirect(redirect_url)
    apps, tags = get_apps_and_tags(access_group)

    wiki_tags_db = WikiTags.query.all()
    return render_template(
        "docs_system/wiki-tags.html",
        access_group=access_group,
        apps=apps,
        tags=tags,
        wiki_tags=wiki_tags_db,
    )


@docs_system.route("/wikis", methods=["GET"])
def wikis():
    access_group, redirect_url = get_access_group(current_user, page="wikis")
    if redirect_url:
        return redirect(redirect_url)
    apps, tags = get_apps_and_tags(access_group)

    if request.args.get("tag", None):
        tag = WikiTags.query.filter_by(id=request.args.get("tag")).first()
        wikis_db = tag.wikis
    else:
        tag = None
        wikis_db = Wiki.query.all()
    for wiki_db in wikis_db:
        wiki_db.updated_moment = create_moment(wiki_db.updated)
    return render_template(
        "docs_system/wikis.html",
        access_group=access_group,
        apps=apps,
        tags=tags,
        wikis=wikis_db,
        tag=tag,
    )


@docs_system.route("/wiki-<permalink>", methods=["GET"])
def wiki(permalink=None):
    access_group, redirect_url = get_access_group(current_user, page="wiki")
    if redirect_url:
        return redirect(redirect_url)
    apps, tags = get_apps_and_tags(access_group)

    wiki_db = Wiki.query.filter_by(permalink=permalink).first()
    if wiki_db:
        wiki_fp = os.path.join(wiki_folder, f"{wiki_db.name}.md")
        with open(wiki_fp, "r") as file:
            wiki_md = file.read()
        wiki_md_html = get_md_from_file(file=wiki_db.name, full_path=wiki_fp)
    else:
        wiki_md_html = None

    if wiki_db.wiki_tags.count() > 0:
        wiki_db.tags_str = ",".join([tag.name for tag in wiki_db.wiki_tags])
    return render_template(
        "docs_system/wiki.html",
        access_group=access_group,
        wiki=wiki_db,
        wiki_md_html=wiki_md_html,
        wiki_md=wiki_md,
        apps=apps,
        tags=tags,
    )


@docs_system.route("/save_wiki", methods=["POST"])
def save_wiki():
    create_edit_wiki(
        permalink=request.form.get("wiki_permalink", None),
        permalink_new=request.form.get("wiki_permalink_new", None),
        name=request.form.get("wiki_name", None),
        author=request.form.get("wiki_author", None),
        description=request.form.get("wiki_description", None),
        md=request.form.get("config", None),
        tags=request.form.get("wiki_tags", None),
    )
    return "ok"
