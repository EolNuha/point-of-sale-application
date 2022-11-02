from flask import Blueprint, request, jsonify, request
from website.models import Product, Notification
from website.json import getProductsList, getNotificationList
from website.helpers import getPaginatedDict
from datetime import datetime, timedelta, date, time
from website import db
from sqlalchemy import asc, desc

notification = Blueprint('notification', __name__)

@notification.route('/notifications', methods=["GET"])
def getNotifications():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    sort_column = request.args.get('sort_column', "date_created", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)

    sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

    paginated_items = Notification.query.order_by(
            Notification.date_created.desc()
        ).order_by(sort).paginate(page=page, per_page=per_page)
    return jsonify(getPaginatedDict(getNotificationList(paginated_items.items), paginated_items))

@notification.route('/notifications', methods=["POST"])
def updateNotifications():
    notifications = request.json["notifications"]
    for item in notifications:
        notification_record = Notification.query.filter_by(id=item["id"]).first()
        notification_record.notification_read = item["read"]
        db.session.commit()
    return "success", 200

@notification.route('/notifications/<int:id>', methods=["POST"])
def updateNotification(id):
    read = request.json["read"]
    notification_info = Notification.query.filter_by(id=id).first()
    notification_info.notification_read = read
    db.session.commit()
    return "Success", 200

@notification.route('/notifications/product-expire', methods=["GET"])
def checkProductExpireNotification():
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
                    notification_type="product_expire",
                    date_created=datetime.now(),
                    date_modified=datetime.now(),
                )
            )
            db.session.commit()

    
    for product in expired_products:
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
                    notification_type="product_expire",
                    date_created=datetime.now(),
                    date_modified=datetime.now(),
                )
            )
            db.session.commit()
    return "success", 200