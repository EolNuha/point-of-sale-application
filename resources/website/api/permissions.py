from flask import Blueprint, request, jsonify, request
from website.models.permissions import Permissions
from website.jsonify.permissions import getPermissionsList
from datetime import datetime
from website import db
from website.token import currentUser

permissions_api = Blueprint('permissions_api', __name__)

@permissions_api.route('/permissions', methods=["POST"])
def createPermission():
    user_role = request.json["user_role"]
    subject = request.json["subject"]
    action = request.json["action"]

    permission = Permissions(
        subject=subject.lower(), 
        action=action.lower(), 
        key=f"{subject}.{action}", 
        user_role=user_role,
        date_created=datetime.now(),
        date_modified=datetime.now(),
    )

    db.session.add(permission)
    db.session.commit()
    data = {
        "permissionId": permission.id 
    }
    return jsonify(data), 200

@permissions_api.route('/permissions', methods=["GET"])
def getUserPermissions():
    current_user = currentUser(request)
    return jsonify(getPermissionsList(Permissions.query.filter_by(user_role=current_user.user_role).all()))


@permissions_api.route('/permissions/all', methods=["GET"])
def getPermissionsAll():
    p = Permissions.query.with_entities(
            Permissions.id.label("id"), 
            Permissions.date_created.label("date_created"), 
            Permissions.date_modified.label("date_modified"),
            Permissions.subject.label("subject"),
            Permissions.action.label("action"),
            Permissions.key.label("key"),
        )\
        .group_by(Permissions.subject, Permissions.action).all()
    return jsonify(getPermissionsList(p))

@permissions_api.route('/permissions/<string:user_role>', methods=["GET"])
def getUserRolePermissions(user_role):
    return jsonify(getPermissionsList(Permissions.query.filter_by(user_role=user_role).all()))


@permissions_api.route('/permissions', methods=["PUT"])
def updatePermission():
    user_role = request.json["user_role"]
    key = request.json["key"]

    query = Permissions.query.filter_by(user_role=user_role).filter_by(key=key)
    if query.first():
        query.delete()
        db.session.commit()
    else:
        split_key = key.split(".")
        db.session.add(Permissions(user_role=user_role, key=key, subject=split_key[0], action=split_key[1], 
            date_created=datetime.now(),
            date_modified=datetime.now(),))
        db.session.commit()
    return "success", 200

@permissions_api.before_app_first_request
def createDemoSettings():
    if(Permissions.query.count() > 0):
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
        db.session.add(Permissions(
            user_role=i[0],
            subject=i[1],
            action=i[3],
            key=i[2],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            ))
        db.session.commit()
    return "success", 200