from flask import Blueprint
from website.models.user import User
from website.models.product import Product
from website.models.notification import Notification
from website.models.settings import Settings
from website.models.permissions import Permissions
from datetime import datetime, timedelta, date, time
from website import db
from werkzeug.security import generate_password_hash
import uuid

before_app_requests_api = Blueprint("before_app_requests_api", __name__)


@before_app_requests_api.before_app_first_request
def createDemoUsers():
    if User.query.count() > 0:
        return
    demo = [
        ["eol", "nuha", "eolnuha", "eol@gmail.com", "superadmin"],
    ]
    for i in demo:
        db.session.add(
            User(
                public_id=str(uuid.uuid4()),
                first_name=i[0],
                last_name=i[1],
                username=i[2],
                email=i[3],
                password=generate_password_hash("admin"),
                user_role=i[4],
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )
        )
        db.session.commit()
    return "success", 200


@before_app_requests_api.before_app_first_request
def createDemoSettings():
    if Permissions.query.count() > 0:
        return
    demo = [
        ["superadmin", "dashboard", "dashboard.read", "read"],
        ["superadmin", "dashboard", "dashboard.write", "write"],
        ["superadmin", "dashboard", "dashboard.execute", "execute"],
        ["superadmin", "products", "products.read", "read"],
        ["superadmin", "products", "products.write", "write"],
        ["superadmin", "products", "products.execute", "execute"],
        ["superadmin", "sales", "sales.read", "read"],
        ["superadmin", "sales", "sales.write", "write"],
        ["superadmin", "sales", "sales.execute", "execute"],
        ["superadmin", "purchases", "purchases.read", "read"],
        ["superadmin", "purchases", "purchases.write", "write"],
        ["superadmin", "purchases", "purchases.execute", "execute"],
        ["superadmin", "users", "users.read", "read"],
        ["superadmin", "users", "users.write", "write"],
        ["superadmin", "users", "users.execute", "execute"],
        ["superadmin", "analytics", "analytics.read", "read"],
        ["superadmin", "analytics", "analytics.write", "write"],
        ["superadmin", "analytics", "analytics.execute", "execute"],
        ["superadmin", "notifications", "notifications.read", "read"],
        ["superadmin", "notifications", "notifications.write", "write"],
        ["superadmin", "notifications", "notifications.execute", "execute"],
        ["superadmin", "permissions", "permissions.read", "read"],
        ["superadmin", "permissions", "permissions.write", "write"],
        ["superadmin", "permissions", "permissions.execute", "execute"],
    ]
    for i in demo:
        db.session.add(
            Permissions(
                user_role=i[0],
                subject=i[1],
                action=i[3],
                key=i[2],
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )
        )
        db.session.commit()
    return "success", 200


@before_app_requests_api.before_app_first_request
def createDemoSettings():
    if Settings.query.count() > 0:
        return
    demo = [
        ["storage", "storage", "notification", 1500],
        ["pcs", "pcs", "measure", "pcs"],
        ["kg", "kg", "measure", "kg"],
        ["liter", "liter", "measure", "liter"],
        ["purchase", "purchase", "purchasetype", "purchase"],
        ["investment", "investment", "purchasetype", "investment"],
        ["expense", "expense", "purchasetype", "expense"],
        ["8", "eight", "tax", 8],
        ["18", "eighteen", "tax", 18],
    ]
    for i in demo:
        db.session.add(
            Settings(
                settings_name=i[0],
                settings_alias=i[1],
                settings_type=i[2],
                settings_value=i[3],
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )
        )
        db.session.commit()
    return "success", 200


@before_app_requests_api.before_app_first_request
def checkProductExpireNotification():
    storage = (
        Settings.query.filter_by(settings_type="notification")
        .filter_by(settings_name="storage")
        .first()
        .settings_value
    )
    if Notification.query.count() >= int(storage):
        return "Nothing added", 200

    date_start = datetime.combine(date.today(), time.min) + timedelta(days=1)
    date_end = datetime.combine(date.today(), time.max) + timedelta(days=4)
    today_beginning = datetime.combine(date.today(), time.min)
    today_end = datetime.combine(date.today(), time.max)

    almost_expired_products = (
        Product.query.filter()
        .filter(Product.expiration_date <= date_end)
        .filter(Product.expiration_date >= date_start)
        .all()
    )
    expired_products = (
        Product.query.filter()
        .filter(Product.expiration_date <= today_end)
        .filter(Product.expiration_date >= today_beginning)
        .all()
    )

    for product in almost_expired_products:
        if Notification.query.count() >= int(storage):
            return

        time_diff = product.expiration_date - datetime.now()
        message = f"Product {product.name} expires in {time_diff.days + 1} days"
        notification_exists = (
            Notification.query.filter_by(notification_message=message)
            .filter(Notification.date_created <= today_end)
            .filter(Notification.date_created > today_beginning)
            .first()
        )

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
        notification_exists = (
            Notification.query.filter_by(notification_message=message)
            .filter(Notification.date_created <= today_end)
            .filter(Notification.date_created > today_beginning)
            .first()
        )

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
