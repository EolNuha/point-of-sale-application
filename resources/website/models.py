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
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Integer)
    customer_amount = db.Column(db.Integer)
    change_amount = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())