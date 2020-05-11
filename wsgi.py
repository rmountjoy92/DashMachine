#!/usr/bin/env python3

import os

root_folder = os.path.dirname(__file__)
db_file_path = os.path.join(root_folder, "dashmachine", "user_data", "site.db")
try:
    os.remove(db_file_path)
except FileNotFoundError:
    pass

from dashmachine import app
from dashmachine.main.utils import dashmachine_init

dashmachine_init()

if __name__ == "__main__":
    app.run()
