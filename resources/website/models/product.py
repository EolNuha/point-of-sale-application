from .. import db
from datetime import datetime
from sqlalchemy import Index

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(200), unique=True)
    stock = db.Column(db.Numeric(precision=10, scale=4), default=0)
    tax=db.Column(db.Integer, default=0)
    purchased_price_wo_tax = db.Column(db.Numeric(precision=10, scale=4), default=0)
    purchased_price = db.Column(db.Numeric(precision=10, scale=4), default=0)
    selling_price = db.Column(db.Numeric(precision=10, scale=4), default=0)
    measure = db.Column(db.String(50))
    expiration_date = db.Column(db.DateTime, default=None)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())

Index('ix_products', Product.name.asc(), Product.barcode.asc(), Product.id.asc(), unique=True)
Index('ix_product_name', Product.name.asc(), unique=True)
Index('ix_product_id', Product.id.asc(), unique=True)
Index('ix_product_barcode', Product.barcode.asc(), unique=True)
