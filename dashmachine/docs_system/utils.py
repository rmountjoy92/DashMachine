import os
from markdown2 import markdown
from flask import render_template_string, url_for
from dashmachine.paths import docs_folder
from dashmachine.docs_system.core_docs import (
    base_md_string,
    doc_toc_string,
    apps_doc_dict,
    custom_card_doc_dict,
    collections_doc_dict,
)


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
