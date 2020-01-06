from dashmachine import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    fname = db.Column(db.String())
    lname = db.Column(db.String())
    phone = db.Column(db.String())
    avatar = db.Column(db.String())
    role = db.Column(db.String())


db.create_all()
db.session.commit()
