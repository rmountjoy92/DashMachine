from dashmachine import db


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String())
    accent = db.Column(db.String())
    background = db.Column(db.String())


db.create_all()
db.session.commit()
