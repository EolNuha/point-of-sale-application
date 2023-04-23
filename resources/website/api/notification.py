from flask import Blueprint, request, jsonify, request
from website.models.product import Product
from website.models.notification import Notification
from website.models.settings import Settings
from website.jsonify.notification import getNotificationList
from website.helpers import getPaginatedDict
from datetime import datetime, timedelta, date, time
from website import db
from sqlalchemy import asc, desc

notification_api = Blueprint('notification_api', __name__)

@notification_api.route('/notifications', methods=["GET"])
def getNotifications():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    col_name = request.args.get('col_name', None, type=str)
    sort_column = request.args.get('sort_column', "date_created", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)

    sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

    query = Notification.query.order_by(sort)

    if col_name == 'read':
        query = query.filter_by(notification_read=False)
    elif col_name == 'star':
        query = query.filter_by(notification_star=True)
    
    paginated_items = query.paginate(page=page, per_page=per_page)
    return jsonify(getPaginatedDict(getNotificationList(paginated_items.items), paginated_items))

@notification_api.route('/notifications', methods=["POST"])
def updateNotifications():
    notifications = request.json["notifications"]
    for item in notifications:
        notification_record = Notification.query.filter_by(id=item["id"]).first()
        notification_record.notification_read = item["read"]
        notification_record.notification_star = item["star"]
        db.session.commit()
    return "success", 200

@notification_api.route('/notifications/<int:id>', methods=["DELETE"])
def deleteNotification(id):
    Notification.query.filter_by(id=id).delete()
    db.session.commit()
    return "success", 200

@notification_api.route('/notifications', methods=["DELETE"])
def deleteNotifications():
    notifications = request.json["notifications"]
    for item in notifications:
        Notification.query.filter_by(id=item["id"]).delete()
        db.session.commit()
    return "success", 200

@notification_api.route('/notifications/<int:id>', methods=["POST"])
def updateNotification(id):
    read = request.json["read"]
    star = request.json["star"]
    notification_info = Notification.query.filter_by(id=id).first()
    if read != None:
        notification_info.notification_read = read
    if star != None:
        notification_info.notification_star = star
    db.session.commit()
    return "Success", 200

@notification_api.before_app_first_request
def checkProductExpireNotification():
    storage = Settings.query.filter_by(settings_type="notification").filter_by(settings_name="storage").first().settings_value
    if Notification.query.count() >= int(storage):
        return "Nothing added", 200

    date_start = datetime.combine(date.today(), time.min) + timedelta(days=1)
    date_end = datetime.combine(date.today(), time.max) + timedelta(days=4)
    today_beginning = datetime.combine(date.today(), time.min)
    today_end = datetime.combine(date.today(), time.max)

    almost_expired_products = Product.query.filter()\
        .filter(Product.expiration_date <= date_end)\
        .filter(Product.expiration_date >= date_start)\
        .all()
    expired_products = Product.query.filter()\
        .filter(Product.expiration_date <= today_end)\
        .filter(Product.expiration_date >= today_beginning)\
        .all()
    
    for product in almost_expired_products:
        if Notification.query.count() >= int(storage):
            return "Nothing added", 200
        
        time_diff = product.expiration_date - datetime.now()
        message = f"Product {product.name} expires in {time_diff.days + 1} days"
        notification_exists = Notification.query.filter_by(notification_message=message)\
            .filter(Notification.date_created <= today_end)\
            .filter(Notification.date_created > today_beginning)\
            .first()
        
        if not notification_exists:
            db.session.add(
                Notification(
                    notification_to_id=product.id,
                    notification_message=message,
                    notification_type="Product Expiration",
                    date_created=datetime.now(),
                    date_modified=datetime.now(),
                )
            )
            db.session.commit()

    
    for product in expired_products:
        if Notification.query.count() >= int(storage):
            return "Nothing added", 200

        message = f"Product {product.name} has expired"
        notification_exists = Notification.query.filter_by(notification_message=message)\
            .filter(Notification.date_created <= today_end)\
            .filter(Notification.date_created > today_beginning)\
            .first()
        
        if not notification_exists:
            db.session.add(
                Notification(
                    notification_to_id=product.id,
                    notification_message=message,
                    notification_type="Product Expiration",
                    date_created=datetime.now(),
                    date_modified=datetime.now(),
                )
            )
            db.session.commit()
    return "success", 200