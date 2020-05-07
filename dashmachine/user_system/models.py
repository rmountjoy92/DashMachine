from dashmachine import db, login_manager
from flask_login import UserMixin


rel_apps_access_groups = db.Table(
    "rel_apps_access_groups",
    db.Column("access_group_id", db.Integer, db.ForeignKey("access_groups.id")),
    db.Column("app_id", db.Integer, db.ForeignKey("apps.id")),
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    confirm_password = db.Column(db.String(60))
    role = db.Column(db.String())
    theme = db.Column(db.String())
    background = db.Column(db.String())
    accent = db.Column(db.String())
    tags_expanded = db.Column(db.String())


class AccessGroups(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    roles = db.Column(db.String())
    can_access_home = db.Column(db.String(), default="True")
    can_access_user_settings = db.Column(db.String(), default="True")
    can_access_main_settings = db.Column(db.String(), default="False")
    can_access_card_editor = db.Column(db.String(), default="False")
    can_access_raw_config = db.Column(db.String(), default="False")
    can_access_docs = db.Column(db.String(), default="False")
    can_see_sidenav = db.Column(db.String(), default="True")
    can_edit_users = db.Column(db.String(), default="False")
    can_edit_images = db.Column(db.String(), default="False")
    apps = db.relationship(
        "Apps",
        secondary=rel_apps_access_groups,
        backref=db.backref("access_groups", lazy="dynamic"),
    )
