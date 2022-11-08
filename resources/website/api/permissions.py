from flask import Blueprint, request, jsonify, request
from website.models import Permissions
from website.json import getPermissionsList
from datetime import datetime
from website import db
from website.token import currentUser

permissions = Blueprint('permissions', __name__)

@permissions.route('/permissions', methods=["GET"])
def getUserPermissions():
    current_user = currentUser(request)
    return jsonify(getPermissionsList(Permissions.query.filter_by(user_type=current_user.user_type).all()))

@permissions.route('/permissions/demo', methods=["GET"])
def createDemoSettings():
    demo = [
        ["superadmin", "dashboard", "dashboard.read", "read"],
        ["superadmin", "dashboard", "dashboard.write", "write"],
        ["superadmin", "dashboard", "dashboard.execute", "execute"],
        ["superadmin", "product", "product.read", "read"],
        ["superadmin", "product", "product.write", "write"],
        ["superadmin", "product", "product.execute", "execute"],
        ["superadmin", "sale", "sale.read", "read"],
        ["superadmin", "sale", "sale.write", "write"],
        ["superadmin", "sale", "sale.execute", "execute"],
        ["superadmin", "purchase", "purchase.read", "read"],
        ["superadmin", "purchase", "purchase.write", "write"],
        ["superadmin", "purchase", "purchase.execute", "execute"],
        ["superadmin", "user", "user.read", "read"],
        ["superadmin", "user", "user.write", "write"],
        ["superadmin", "user", "user.execute", "execute"],
        ["superadmin", "analytics", "analytics.read", "read"],
        ["superadmin", "analytics", "analytics.write", "write"],
        ["superadmin", "analytics", "analytics.execute", "execute"],
        ["superadmin", "notification", "notification.read", "read"],
        ["superadmin", "notification", "notification.write", "write"],
        ["superadmin", "notification", "notification.execute", "execute"],
        
        ["owner", "dashboard", "dashboard.read", "read"],
        ["owner", "dashboard", "dashboard.write", "write"],
        ["owner", "dashboard", "dashboard.execute", "execute"],
        ["owner", "product", "product.read", "read"],
        ["owner", "product", "product.write", "write"],
        ["owner", "product", "product.execute", "execute"],
        ["owner", "sale", "sale.read", "read"],
        ["owner", "sale", "sale.write", "write"],
        ["owner", "sale", "sale.execute", "execute"],
        ["owner", "purchase", "purchase.read", "read"],
        ["owner", "purchase", "purchase.write", "write"],
        ["owner", "purchase", "purchase.execute", "execute"],
        ["owner", "user", "user.read", "read"],
        ["owner", "user", "user.write", "write"],
        ["owner", "user", "user.execute", "execute"],
        ["owner", "analytics", "analytics.read", "read"],
        ["owner", "analytics", "analytics.write", "write"],
        ["owner", "analytics", "analytics.execute", "execute"],
        ["owner", "notification", "notification.read", "read"],
        ["owner", "notification", "notification.write", "write"],
        ["owner", "notification", "notification.execute", "execute"],
        
        ["manager", "dashboard", "dashboard.read", "read"],
        ["manager", "dashboard", "dashboard.write", "write"],
        ["manager", "dashboard", "dashboard.execute", "execute"],
        ["manager", "product", "product.read", "read"],
        ["manager", "product", "product.write", "write"],
        ["manager", "product", "product.execute", "execute"],
        ["manager", "sale", "sale.read", "read"],
        ["manager", "sale", "sale.write", "write"],
        ["manager", "purchase", "purchase.read", "read"],
        ["manager", "purchase", "purchase.write", "write"],
        ["manager", "user", "user.read", "read"],
        ["manager", "analytics", "analytics.read", "read"],
        ["manager", "notification", "notification.read", "read"],
        ["manager", "notification", "notification.write", "write"],
        
        ["staff", "dashboard", "dashboard.read", "read"],
        ["staff", "dashboard", "dashboard.write", "write"],
        ["staff", "product", "product.read", "read"],
        ["staff", "sale", "sale.read", "read"],
        ["staff", "sale", "sale.write", "write"],
        ["staff", "purchase", "purchase.read", "read"],
        ["staff", "user", "user.read", "read"],
        ["staff", "analytics", "analytics.read", "read"],
        ["staff", "notification", "notification.read", "read"],
    ]
    for i in demo:
        db.session.add(Permissions(
            user_type=i[0],
            subject=i[1],
            action=i[3],
            key=i[2],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            ))
        db.session.commit()
    return "success", 200