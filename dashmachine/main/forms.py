from flask_wtf import FlaskForm
from wtforms import SelectField


class TagsForm(FlaskForm):
    tags = SelectField(choices=[("All tags", "All tags")])
