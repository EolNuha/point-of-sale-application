from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api
import os

db = SQLAlchemy()
swagger = Api()
migrate = Migrate()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = "D2GECauenaubK6eA1JWwJ7Lpo7C2Ta4P"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    db.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db)

    from website.api.before_app_requests import before_app_requests_api
    from website.api.product import product_rest
    from website.api.sale import sale_rest
    from website.api.purchase import purchase_rest
    from website.api.auth import auth_api, auth_rest
    from website.api.analytics import analytics_rest
    from website.api.settings import settings_rest
    from website.api.notification import notification_rest
    from website.api.permissions import permissions_rest

    app.register_blueprint(before_app_requests_api, url_prefix="/api/")
    app.register_blueprint(auth_api, url_prefix="/")
    swagger.add_namespace(auth_rest, path="/")
    swagger.add_namespace(settings_rest, path="/api/")
    swagger.add_namespace(notification_rest, path="/api/")
    swagger.add_namespace(permissions_rest, path="/api/")
    swagger.add_namespace(product_rest, path="/api/")
    swagger.add_namespace(analytics_rest, path="/api/")
    swagger.add_namespace(sale_rest, path="/api/")
    swagger.add_namespace(purchase_rest, path="/api/")

    create_database(app)

    return app


def create_database(app):
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app=app)
