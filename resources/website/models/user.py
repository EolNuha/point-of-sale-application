from .. import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    user_role = db.Column(db.Enum("staff", "manager", "owner", "superadmin"), default="staff")
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())
    sales = db.relationship('Sale', backref='user', lazy=True)
    purchases = db.relationship('Purchase', backref='user', lazy=True)