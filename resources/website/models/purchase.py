from .. import db
from datetime import datetime

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_name = db.Column(db.String(200))
    seller_invoice_number = db.Column(db.String(200))
    seller_fiscal_number = db.Column(db.Integer)
    seller_tax_number = db.Column(db.Integer)
    total_amount = db.Column(db.Numeric(precision=10, scale=2))
    subtotal_amount = db.Column(db.Numeric(precision=10, scale=2))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    purchase_taxes = db.relationship('PurchaseTax', backref='purchase', lazy=True)
    purchase_items = db.relationship('PurchaseItem', backref='purchase', lazy=True)

class PurchaseTax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    tax_name = db.Column(db.String(200))
    tax_alias = db.Column(db.String(200))
    tax_value = db.Column(db.Numeric(precision=10, scale=2))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())

class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    product_id = db.Column(db.Integer)
    product_barcode = db.Column(db.Integer)
    product_name = db.Column(db.String(200))
    product_tax=db.Column(db.Integer, default=18)
    product_purchased_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    product_selling_price = db.Column(db.Numeric(precision=10, scale=2), default=0)
    product_stock = db.Column(db.Numeric(precision=10, scale=2))
    price_without_tax = db.Column(db.Numeric(precision=10, scale=2))
    tax_amount = db.Column(db.Numeric(precision=10, scale=2))
    total_amount = db.Column(db.Numeric(precision=10, scale=2), default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())