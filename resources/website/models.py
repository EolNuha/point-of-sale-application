from . import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(200))
    stock = db.Column(db.Numeric(precision=10, scale=2), default=0)
    tax=db.Column(db.Integer, default=18)
    purchased_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    selling_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Numeric(precision=10, scale=2))
    subtotal_amount = db.Column(db.Numeric(precision=10, scale=2))
    eight_tax_amount = db.Column(db.Numeric(precision=10, scale=2))
    eighteen_tax_amount = db.Column(db.Numeric(precision=10, scale=2))
    customer_amount = db.Column(db.Numeric(precision=10, scale=2))
    change_amount = db.Column(db.Numeric(precision=10, scale=2))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer)
    product_barcode = db.Column(db.Integer)
    product_name = db.Column(db.String(200))
    product_tax=db.Column(db.Integer, default=18)
    product_purchased_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    product_selling_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    product_quantity = db.Column(db.Numeric(precision=10, scale=2))
    price_without_tax = db.Column(db.Numeric(precision=10, scale=2))
    tax_amount = db.Column(db.Numeric(precision=10, scale=2))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())