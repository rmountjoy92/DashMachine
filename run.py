#!/usr/bin/env python3

import os

root_folder = os.path.dirname(__file__)

os.system("python " + os.path.join(root_folder, "manage_db.py db migrate"))

os.system("python " + os.path.join(root_folder, "manage_db.py db upgrade"))

from dashmachine import app
from dashmachine.main.utils import dashmachine_init

dashmachine_init()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", threaded=True)
