from .. import db
from datetime import datetime
from sqlalchemy import Index

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gross_profit_amount = db.Column(db.Numeric(precision=10, scale=4))
    net_profit_amount = db.Column(db.Numeric(precision=10, scale=4))
    total_amount = db.Column(db.Numeric(precision=10, scale=4))
    subtotal_amount = db.Column(db.Numeric(precision=10, scale=4))
    customer_amount = db.Column(db.Numeric(precision=10, scale=4))
    change_amount = db.Column(db.Numeric(precision=10, scale=4))
    is_regular = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    sale_taxes = db.relationship('SaleTax', backref='sale', lazy=True)
    sale_items = db.relationship('SaleItem', backref='sale', lazy=True)

class SaleTax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    tax_name = db.Column(db.String(200))
    tax_alias = db.Column(db.String(200))
    tax_value = db.Column(db.Numeric(precision=10, scale=4))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer)
    product_barcode = db.Column(db.Integer)
    product_name = db.Column(db.String(200))
    product_tax=db.Column(db.Integer, default=18)
    product_purchased_price = db.Column(db.Numeric(precision=10, scale=4), default=0)
    product_selling_price = db.Column(db.Numeric(precision=10, scale=4), default=0)
    product_quantity = db.Column(db.Numeric(precision=10, scale=4))
    price_without_tax = db.Column(db.Numeric(precision=10, scale=4))
    product_measure = db.Column(db.Enum("pcs", "kg", "liter"), default="pcs")
    tax_amount = db.Column(db.Numeric(precision=10, scale=4))
    total_amount = db.Column(db.Numeric(precision=10, scale=4))
    gross_profit_amount = db.Column(db.Numeric(precision=10, scale=4))
    net_profit_amount = db.Column(db.Numeric(precision=10, scale=4))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())

Index('ix_sales', Sale.id.asc(), Sale.total_amount.asc(), Sale.subtotal_amount.asc(), Sale.date_created.asc())