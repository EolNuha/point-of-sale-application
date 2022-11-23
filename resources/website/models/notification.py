from .. import db
from datetime import datetime

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notification_to_id = db.Column(db.Integer)
    notification_message = db.Column(db.String(200))
    notification_type = db.Column(db.String(200))
    notification_read = db.Column(db.Boolean, default=False)
    notification_star = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.now())