#!/usr/bin/env python3
import os
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from dashmachine.paths import user_data_folder

if not os.path.isdir(user_data_folder):
    os.mkdir(user_data_folder)

context_path = os.getenv("CONTEXT_PATH", "")
app = Flask(__name__, static_url_path=context_path + "/static")
cache = Cache(app, config={"CACHE_TYPE": "simple"})
api = Api(app)

app.config["AVATARS_IDENTICON_BG"] = (255, 255, 255)
app.config["SECRET_KEY"] = "66532a62c4048f976e22a39638b6f10e"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_data/site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")

from dashmachine.main.routes import main
from dashmachine.user_system.routes import user_system
from dashmachine.error_pages.routes import error_pages
from dashmachine.settings_system.routes import settings_system
from dashmachine import sources

app.register_blueprint(main, url_prefix=context_path)
app.register_blueprint(user_system, url_prefix=context_path)
app.register_blueprint(error_pages, url_prefix=context_path)
app.register_blueprint(settings_system, url_prefix=context_path)


from dashmachine.rest_api.resources import *

api.add_resource(GetVersion, "/api/version")
