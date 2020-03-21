import os
from dashmachine import bcrypt
from dashmachine.paths import auth_cache
from dashmachine.user_system.models import User


def hash_and_cache_password(password, user_id):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    with open(os.path.join(auth_cache, str(user_id)), "w") as cache_file:
        cache_file.write(hashed_password)
    return hashed_password


def get_cached_password(user_id):
    try:
        with open(os.path.join(auth_cache, str(user_id)), "r") as cache_file:
            password = cache_file.read()
    except FileNotFoundError:
        return hash_and_cache_password("admin", user_id)
    return password


def clean_auth_cache():
    for file in os.listdir(auth_cache):
        if not User.query.filter_by(id=file).first():
            os.remove(os.path.join(auth_cache, file))
