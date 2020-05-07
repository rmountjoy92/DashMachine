from dashmachine import db


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String())
    accent = db.Column(db.String())
    background = db.Column(db.String())
    roles = db.Column(db.String())
    custom_app_title = db.Column(db.String())
    tags_expanded = db.Column(db.String())
    action_providers = db.Column(db.String())
    tags = db.Column(db.String())
