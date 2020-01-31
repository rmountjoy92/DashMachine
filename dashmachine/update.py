import os
import subprocess
from dashmachine.paths import root_folder

migrate_fn = os.path.join(root_folder, 'manage_db.py db migrate')
upgrade_fn = os.path.join(root_folder, 'manage_db.py db upgrade')

def update():
