from .. import db
from datetime import datetime

class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.Enum("staff", "manager", "owner", "superadmin"), default="staff")
    subject = db.Column(db.String(200))
    action = db.Column(db.String(200))
    key = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())