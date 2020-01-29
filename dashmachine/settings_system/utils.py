from dashmachine.paths import backgrounds_images_folder, icons_images_folder
from flask import render_template
from os import listdir


def load_files_html():
    backgrounds = listdir(backgrounds_images_folder)
    icons = listdir(icons_images_folder)
    return render_template(
        "settings_system/files.html",
        backgrounds=backgrounds,
        icons=icons,
    )
