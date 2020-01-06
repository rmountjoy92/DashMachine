from dashmachine.paths import backgrounds_images_folder, apps_images_folder
from flask import render_template
from os import listdir


def load_files_html():
    background_images = listdir(backgrounds_images_folder)
    apps_images = listdir(apps_images_folder)
    return render_template(
        "settings_system/files.html",
        background_images=background_images,
        apps_images=apps_images,
    )
