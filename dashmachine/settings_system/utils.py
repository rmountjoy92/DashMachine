import os
import importlib
from markdown2 import markdown
from dashmachine.paths import (
    backgrounds_images_folder,
    icons_images_folder,
    root_folder,
    platform_folder,
)
from flask import render_template


def load_files_html():
    backgrounds = os.listdir(backgrounds_images_folder)
    icons = os.listdir(icons_images_folder)
    return render_template(
        "settings_system/files.html", backgrounds=backgrounds, icons=icons,
    )


def get_config_html():
    with open(os.path.join(root_folder, "config_readme.md")) as readme_file:
        md = readme_file.read()
    platforms = os.listdir(platform_folder)
    platforms = sorted(platforms)
    for platform in platforms:
        name, extension = os.path.splitext(platform)
        if extension.lower() == ".py":
            module = importlib.import_module(f"dashmachine.platform.{name}", ".")
            if module.__doc__:
                md += module.__doc__

    config_html = markdown(
        md,
        extras=[
            "tables",
            "fenced-code-blocks",
            "break-on-newline",
            "header-ids",
            "code-friendly",
        ],
    )
    return config_html
