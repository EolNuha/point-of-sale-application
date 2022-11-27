from .. import db
from datetime import datetime

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Numeric(precision=10, scale=2))
    subtotal_amount = db.Column(db.Numeric(precision=10, scale=2))
    customer_amount = db.Column(db.Numeric(precision=10, scale=2))
    change_amount = db.Column(db.Numeric(precision=10, scale=2))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    sale_taxes = db.relationship('SaleTax', backref='sale', lazy=True)
    sale_items = db.relationship('SaleItem', backref='sale', lazy=True)

class SaleTax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    tax_name = db.Column(db.String(200))
    tax_alias = db.Column(db.String(200))
    tax_value = db.Column(db.Numeric(precision=10, scale=2))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer)
    product_barcode = db.Column(db.Integer)
    product_name = db.Column(db.String(200))
    product_tax=db.Column(db.Integer, default=18)
    product_purchased_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    product_selling_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    product_quantity = db.Column(db.Numeric(precision=10, scale=2))
    price_without_tax = db.Column(db.Numeric(precision=10, scale=2))
    tax_amount = db.Column(db.Numeric(precision=10, scale=2))
    total_amount = db.Column(db.Numeric(precision=10, scale=2))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())