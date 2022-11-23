from .. import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(200), unique=True)
    stock = db.Column(db.Numeric(precision=10, scale=2), default=0)
    tax=db.Column(db.Integer, default=18)
    purchased_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    selling_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    expiration_date = db.Column(db.DateTime, default=datetime.now())
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
