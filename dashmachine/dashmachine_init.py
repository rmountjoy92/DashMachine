import os
from shutil import copyfile
from dashmachine.paths import dashmachine_folder, images_folder
from dashmachine.main.utils import read_config
from dashmachine.user_system.models import User
from dashmachine.user_system.utils import add_edit_user


def dashmachine_init():
    user_data_folder = os.path.join(dashmachine_folder, "user_data")

    # create the user_data subdirectories, link them to static
    user_backgrounds_folder = os.path.join(user_data_folder, "backgrounds")
    if not os.path.isdir(user_backgrounds_folder):
        os.mkdir(user_backgrounds_folder)
        os.symlink(user_backgrounds_folder, os.path.join(images_folder, "backgrounds"))

    user_icons_folder = os.path.join(user_data_folder, "user_icons")
    if not os.path.isdir(user_icons_folder):
        os.mkdir(user_icons_folder)
        os.symlink(user_icons_folder, os.path.join(images_folder, "user_icons"))

    config_file = os.path.join(user_data_folder, "config.ini")
    if not os.path.exists(config_file):
        copyfile("default_config.ini", config_file)
        read_config()

    user = User.query.first()
    if not user:
        add_edit_user(username="admin", password="admin")
