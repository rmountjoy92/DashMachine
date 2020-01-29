#!/usr/bin/env python3

from dashmachine import app
from dashmachine.main.utils import dashmachine_init

dashmachine_init()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", threaded=True)
