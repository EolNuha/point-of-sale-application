from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'D2GECauenaubK6eA1JWwJ7Lpo7C2Ta4P'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    from website.api.product import product
    from website.api.sale import sale
    from website.api.purchase import purchase_api
    from website.api.auth import auth
    from website.api.analytics import analytics
    from website.api.settings import settings
    from website.api.notification import notification
    from website.api.permissions import permissions

    app.register_blueprint(product, url_prefix='/api/')
    app.register_blueprint(sale, url_prefix='/api/')
    app.register_blueprint(purchase_api, url_prefix='/api/')
    app.register_blueprint(analytics, url_prefix='/api/')
    app.register_blueprint(settings, url_prefix='/api/')
    app.register_blueprint(notification, url_prefix='/api/')
    app.register_blueprint(permissions, url_prefix='/api/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    return app


def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=app)