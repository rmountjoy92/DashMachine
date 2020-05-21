from dashmachine import db

rel_app_data_source = db.Table(
    "rel_app_data_source",
    db.Column("data_source_id", db.Integer, db.ForeignKey("data_sources.id")),
    db.Column("app_id", db.Integer, db.ForeignKey("apps.id")),
)

rel_apps_tags = db.Table(
    "rel_apps_tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
    db.Column("app_id", db.Integer, db.ForeignKey("apps.id")),
)

rel_wiki_wiki_tags = db.Table(
    "rel_wiki_wiki_tags",
    db.Column("wiki_tag_id", db.Integer, db.ForeignKey("wiki_tags.id")),
    db.Column("wiki_id", db.Integer, db.ForeignKey("wiki.id")),
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
    type = db.Column(db.String())
    urls = db.Column(db.String())


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


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    icon = db.Column(db.String())
    sort_pos = db.Column(db.Integer)
    apps = db.relationship(
        "Apps", secondary=rel_apps_tags, backref=db.backref("tags", lazy="dynamic"),
    )


class WikiTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    wikis = db.relationship(
        "Wiki",
        secondary=rel_wiki_wiki_tags,
        backref=db.backref("wiki_tags", lazy="dynamic"),
    )


class Wiki(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    permalink = db.Column(db.String())
    name = db.Column(db.String())
    author = db.Column(db.String())
    description = db.Column(db.String())
    md = db.Column(db.String())
    score = db.Column(db.Integer, default=0)
    created = db.Column(db.String())
    updated = db.Column(db.String())
    url = db.Column(db.String())
