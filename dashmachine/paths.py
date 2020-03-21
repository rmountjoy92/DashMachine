import os
from pathlib import Path


# root path of the application
def get_root_folder():
    curr_folder = os.path.dirname(__file__)
    root_folder = Path(curr_folder).parent
    return root_folder


root_folder = get_root_folder()

dashmachine_folder = os.path.join(root_folder, "dashmachine")

template_apps_folder = os.path.join(root_folder, "template_apps")

platform_folder = os.path.join(dashmachine_folder, "platform")

user_data_folder = os.path.join(dashmachine_folder, "user_data")

auth_cache = os.path.join(user_data_folder, "auth_cache")

if not os.path.isdir(auth_cache):
    os.mkdir(auth_cache)

static_folder = os.path.join(dashmachine_folder, "static")

images_folder = os.path.join(static_folder, "images")

apps_images_folder = os.path.join(images_folder, "apps")

backgrounds_images_folder = os.path.join(images_folder, "backgrounds")

icons_images_folder = os.path.join(images_folder, "icons")

cache_folder = os.path.join(static_folder, "cache")

user_images_folder = os.path.join(images_folder, "user")
