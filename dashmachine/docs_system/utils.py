import os
from shutil import copy2
from secrets import token_hex
from datetime import datetime
from markdown2 import markdown
from configparser import ConfigParser
from flask import render_template_string
from dashmachine import db
from dashmachine.paths import docs_folder, wiki_folder, wiki_config_file, root_folder
from dashmachine.docs_system.core_docs import (
    base_md_string,
    doc_toc_string,
    apps_doc_dict,
    custom_card_doc_dict,
    collections_doc_dict,
)
from dashmachine.main.models import Wiki, WikiTags


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def convert_html_to_md(md):
    html = markdown(
        md,
        extras=[
            "tables",
            "fenced-code-blocks",
            "break-on-newline",
            "header-ids",
            "code-friendly",
        ],
    )
    return html


def get_md_from_file(file, full_path=None):
    if full_path:
        path = full_path
    else:
        path = os.path.join(docs_folder, file)
    with open(path) as readme_file:
        md = readme_file.read()
        html = convert_html_to_md(md)
        return html


def get_md_from_dict(doc_dict):
    rendered_md = render_template_string(base_md_string, doc_dict=doc_dict)
    html = convert_html_to_md(rendered_md)
    return html


def get_toc_md_from_dicts(doc_dicts):
    rendered_md = render_template_string(doc_toc_string, doc_dicts=doc_dicts)
    html = convert_html_to_md(rendered_md)
    return html


def get_card_doc_dict(card_type):
    if card_type == "app":
        card_doc_dict = apps_doc_dict
    if card_type == "collection":
        card_doc_dict = collections_doc_dict
    if card_type == "custom":
        card_doc_dict = custom_card_doc_dict
    return card_doc_dict


def create_edit_wiki(
    permalink=None,
    permalink_new=None,
    name="Unnamed Wiki",
    author=None,
    description=None,
    md="",
    tags=None,
):
    wiki = Wiki.query.filter_by(permalink=permalink).first()
    if not wiki:
        wiki = Wiki()
        if not permalink:
            wiki.permalink = token_hex(12)
        else:
            wiki.permalink = permalink
        wiki.created = datetime.now()
        editing = False
    else:
        editing = True

    if permalink_new:
        wiki.permalink = permalink_new

    wiki.name = name
    wiki.author = author
    wiki.description = description
    wiki.md = md
    wiki.updated = datetime.now()
    if not wiki.created:
        wiki.created = datetime.now()

    if editing:
        db.session.merge(wiki)
    else:
        db.session.add(wiki)
    db.session.commit()

    if tags:
        for tag_name in tags.split(","):
            tag_name = tag_name.strip()
            tag = WikiTags.query.filter_by(name=tag_name).first()
            if not tag:
                tag = WikiTags(name=tag_name)
            tag.wikis.append(wiki)
            db.session.merge(tag)
            db.session.commit()

    create_wiki_files(wiki)


def create_wiki_files(wiki):
    with open(os.path.join(wiki_folder, f"{wiki.name}.md"), "w") as md_file:
        md_file.write(wiki.md)

    config = ConfigParser(interpolation=None)
    config.read(wiki_config_file)
    if wiki.name not in config.sections():
        config.add_section(wiki.name)
    for key, value in row2dict(wiki).items():
        if key not in ["id", "md", "name"]:
            config.set(wiki.name, key, value)

    config.set(wiki.name, "tags", ",".join([tag.name for tag in wiki.wiki_tags]))

    config.write(open(wiki_config_file, "w"))


def build_wiki_from_wiki_folder():
    if not os.path.isdir(wiki_folder):
        os.mkdir(wiki_folder)

    if not os.path.isfile(wiki_config_file):
        default_config = os.path.join(root_folder, "default_wiki_config.ini")
        new_config = os.path.join(wiki_folder, "wiki_config.ini")
        copy2(default_config, new_config)

    config = ConfigParser(interpolation=None)
    config.read(wiki_config_file)

    for section in config.sections():
        if section != "WikiSettings":
            with open(os.path.join(wiki_folder, f"{section}.md"), "r") as file:
                md = file.read()

            wiki = config[section]
            create_edit_wiki(
                name=section,
                author=wiki.get("author", None),
                description=wiki.get("description", None),
                md=md,
                tags=wiki.get("tags", None),
                permalink=wiki.get("permalink", None),
            )
