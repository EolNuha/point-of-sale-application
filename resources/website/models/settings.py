from .. import db
from datetime import datetime


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    settings_name = db.Column(db.String(200))
    settings_alias = db.Column(db.String(200))
    settings_type = db.Column(db.String(200))
    settings_value = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    tax_number = db.Column(db.String(50), nullable=False)
    fiscal_number = db.Column(db.String(50), nullable=False)
    logo = db.Column(db.String(255), nullable=True)

    def __init__(self, name, address, phone, tax_number, fiscal_number, logo):
        self.name = name
        self.address = address
        self.phone = phone
        self.tax_number = tax_number
        self.fiscal_number = fiscal_number
        self.logo = logo
