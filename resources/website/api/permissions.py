from flask import Blueprint, request, request
from website.models.permissions import Permissions
from datetime import datetime
from website import db
from website.token import currentUser
from website.api_models.permissions import permissions_model, permissions_create_model, permissions_update_model
from flask_restx import Resource, Namespace

permissions_api = Blueprint('permissions_api', __name__)
permissions_rest = Namespace('Permissions')

@permissions_rest.route('permissions')
class PermissionsClass(Resource):
    @permissions_rest.marshal_with(permissions_model)
    def get(self):
        current_user = currentUser(request)
        return Permissions.query.filter_by(user_role=current_user.user_role).all()
    
    @permissions_rest.expect(permissions_create_model)
    @permissions_rest.marshal_with(permissions_model)
    def post(self):
        user_role = permissions_rest.payload["user_role"]
        subject = permissions_rest.payload["subject"]
        action = permissions_rest.payload["action"]

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
        return permission, 201
    
    @permissions_rest.expect(permissions_update_model)
    def put(self):
        user_role = permissions_rest.payload["user_role"]
        key = permissions_rest.payload["key"]
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

        return 'Success', 200
        
@permissions_rest.route('permissions/all')
class GetAllPermissions(Resource):
    @permissions_rest.marshal_with(permissions_model)
    def get(self):
        return Permissions.query.with_entities(
            Permissions.id.label("id"), 
            Permissions.date_created.label("date_created"), 
            Permissions.date_modified.label("date_modified"),
            Permissions.subject.label("subject"),
            Permissions.action.label("action"),
            Permissions.key.label("key"),
        )\
        .group_by(Permissions.subject, Permissions.action).all()
@permissions_rest.route('permissions/<string:user_role>')
class GetAllPermissions(Resource):
    @permissions_rest.marshal_with(permissions_model)
    def get(self, user_role):
        return Permissions.query.filter_by(user_role=user_role).all()

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