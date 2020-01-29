from dashmachine import db


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    path = db.Column(db.String())
    external_path = db.Column(db.String())
    cache = db.Column(db.String())
    folder = db.Column(db.String())


class Apps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    prefix = db.Column(db.String())
    url = db.Column(db.String())
    icon = db.Column(db.String())
    sidebar_icon = db.Column(db.String())
    description = db.Column(db.String())
    open_in = db.Column(db.String())
    data_template = db.Column(db.String())


class TemplateApps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    prefix = db.Column(db.String())
    url = db.Column(db.String())
    icon = db.Column(db.String())
    sidebar_icon = db.Column(db.String())
    description = db.Column(db.String())
    open_in = db.Column(db.String())


class ApiCalls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    resource = db.Column(db.String())
    method = db.Column(db.String())
    payload = db.Column(db.String())
    authentication = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String())
    value_template = db.Column(db.String())


db.create_all()
db.session.commit()
