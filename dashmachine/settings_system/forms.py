from flask_wtf import FlaskForm
from wtforms import TextAreaField


class ConfigForm(FlaskForm):
    config = TextAreaField()
