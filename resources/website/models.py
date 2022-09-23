from . import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=0)
    purchased_price = db.Column(db.Integer, default=0)
    selling_price = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())