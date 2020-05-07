#!/usr/bin/env python3

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help='port to listen to (default "5000")', type=int)
args = parser.parse_args()
host_port = args.port
if host_port is None:
    host_port = 5000

file_path = os.path.abspath(__file__)
root_folder = os.path.dirname(file_path)
if not os.path.isdir(os.path.join(root_folder, "dashmachine", "user_data")):
    os.mkdir(os.path.join(root_folder, "dashmachine", "user_data"))
db_file_path = os.path.join(root_folder, "dashmachine", "user_data", "site.db")
try:
    os.remove(db_file_path)
except FileNotFoundError:
    pass


from dashmachine import app
from dashmachine.main.utils import dashmachine_init

dashmachine_init()

if __name__ == "__main__":
    app.run(
        debug=True, use_reloader=True, host="0.0.0.0", port=host_port, threaded=True
    )
