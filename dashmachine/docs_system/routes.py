import os
from flask import render_template, Blueprint, redirect
from flask_login import current_user
from dashmachine.paths import root_folder
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
)
from dashmachine.main.utils import get_apps_and_tags, get_access_group

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
