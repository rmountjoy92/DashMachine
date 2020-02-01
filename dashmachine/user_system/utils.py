from dashmachine import db, bcrypt
from dashmachine.user_system.models import User


def add_edit_user(username, password, user_id=None):
    if user_id:
        user = User.query.filter_by(id=user_id).first()
    else:
        user = User.query.first()
    if not user:
        user = User()

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user.username = username
    user.password = hashed_password
    db.session.merge(user)
    db.session.commit()
