from .. import db
from datetime import datetime
from sqlalchemy import Index

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_name = db.Column(db.String(200))
    seller_invoice_number = db.Column(db.String(200))
    seller_fiscal_number = db.Column(db.Integer)
    seller_tax_number = db.Column(db.Integer)
    purchase_type = db.Column(db.Enum("purchase", "investment", "expense"), default="purchase")
    total_amount = db.Column(db.Numeric(precision=10, scale=4))
    subtotal_amount = db.Column(db.Numeric(precision=10, scale=4))
    rabat_amount = db.Column(db.Numeric(precision=10, scale=4))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    purchase_taxes = db.relationship('PurchaseTax', backref='purchase', lazy=True)
    purchase_items = db.relationship('PurchaseItem', backref='purchase', lazy=True)

class PurchaseTax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    tax_name = db.Column(db.String(200))
    tax_alias = db.Column(db.String(200))
    tax_value = db.Column(db.Numeric(precision=10, scale=4))
    total_without_tax = db.Column(db.Numeric(precision=10, scale=4))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())

class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    product_id = db.Column(db.Integer)
    product_barcode = db.Column(db.Integer)
    product_name = db.Column(db.String(200))
    product_tax=db.Column(db.Integer, default=18)
    product_purchased_price = db.Column(db.Numeric(precision=10, scale=4), default=0)
    product_purchased_price_wo_tax = db.Column(db.Numeric(precision=10, scale=4), default=0)
    product_selling_price = db.Column(db.Numeric(precision=10, scale=4), default=0)
    rabat = db.Column(db.Numeric(precision=3, scale=4), default=0)
    product_measure = db.Column(db.String(50))
    product_stock = db.Column(db.Numeric(precision=10, scale=4))
    tax_amount = db.Column(db.Numeric(precision=10, scale=4))
    total_amount = db.Column(db.Numeric(precision=10, scale=4), default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())

Index('ix_purchases',
    Purchase.id.asc(),
    Purchase.seller_name.asc(),
    Purchase.seller_invoice_number.asc(),
    Purchase.total_amount.asc(),
    Purchase.subtotal_amount.asc(),
    Purchase.date_created.asc()
)