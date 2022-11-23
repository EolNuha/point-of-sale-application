from .. import db
from datetime import datetime

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    settings_name = db.Column(db.String(200))
    settings_alias = db.Column(db.String(200))
    settings_type = db.Column(db.String(200))
    settings_value = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())