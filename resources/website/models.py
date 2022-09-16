from . import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    price = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())
    modified = db.Column(db.DateTime, default=datetime.now())