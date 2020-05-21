from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField


class ConfigForm(FlaskForm):
    config = TextAreaField()
    wiki_name = StringField()
    wiki_permalink_new = StringField()
    wiki_author = StringField()
    wiki_description = TextAreaField()
    wiki_tags = StringField()
