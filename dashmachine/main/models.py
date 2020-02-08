from dashmachine import db

rel_app_data_source = db.Table(
    "rel_app_data_source",
    db.Column("data_source_id", db.Integer, db.ForeignKey("data_sources.id")),
    db.Column("app_id", db.Integer, db.ForeignKey("apps.id")),
)


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
    groups = db.Column(db.String())
    tags = db.Column(db.String())


class TemplateApps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    prefix = db.Column(db.String())
    url = db.Column(db.String())
    icon = db.Column(db.String())
    sidebar_icon = db.Column(db.String())
    description = db.Column(db.String())
    open_in = db.Column(db.String())


class DataSources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    platform = db.Column(db.String())
    args = db.relationship("DataSourcesArgs", backref="data_source")
    apps = db.relationship(
        "Apps",
        secondary=rel_app_data_source,
        backref=db.backref("data_sources", lazy="dynamic"),
    )


class DataSourcesArgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String())
    value = db.Column(db.String())
    data_source_id = db.Column(db.Integer, db.ForeignKey("data_sources.id"))


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    roles = db.Column(db.String())


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
