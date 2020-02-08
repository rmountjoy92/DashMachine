from dashmachine import db, bcrypt
from dashmachine.user_system.models import User


def add_edit_user(username, password, user_id=None, role=None):
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            user = User()
    else:
        user = User()

    admin_users = User.query.filter_by(role="admin").all()
    if user_id and role != "admin" and len(admin_users) < 2:
        return "You must have at least one admin user"

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user.username = username
    user.password = hashed_password
    user.role = role
    db.session.merge(user)
    db.session.commit()
