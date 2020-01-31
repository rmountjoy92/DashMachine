import os
import subprocess
from dashmachine.paths import root_folder


def check_needed():
    subprocess.run("git remote update", shell=True)
    out = subprocess.run(
        "git status -uno", stdout=subprocess.PIPE, shell=True, encoding="utf-8"
    )
    if str(out.stdout).find("Your branch is up to date") > -1:
        needed = False
        return needed

    elif str(out.stdout).find("Your branch is up-to-date") > -1:
        needed = False
        return needed
    else:
        needed = True
        return needed


def update_dashmachine():

    subprocess.run(
        "git pull origin master", stdout=subprocess.PIPE, shell=True, encoding="utf-8"
    )

    migrate_cmd = "python " + os.path.join(root_folder, "manage_db.py db migrate")
    subprocess.run(migrate_cmd, stderr=subprocess.PIPE, shell=True, encoding="utf-8")

    upgrade_cmd = "python " + os.path.join(root_folder, "manage_db.py db upgrade")
    subprocess.run(upgrade_cmd, stderr=subprocess.PIPE, shell=True, encoding="utf-8")
