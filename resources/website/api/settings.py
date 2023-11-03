from flask import Blueprint
from website.models.settings import Settings
from datetime import datetime
from website import db
from flask_restx import Resource, Namespace
from website.api_models.settings import settings_model, settings_input_model

settings_api = Blueprint("settings_api", __name__)
settings_rest = Namespace("Settings")


@settings_rest.route("settings")
class CreateSettings(Resource):
    @settings_rest.expect(settings_input_model)
    @settings_rest.marshal_with(settings_model)
    def post(self):
        settings_name = settings_rest.payload["settings_name"]
        settings_alias = settings_rest.payload["settings_alias"]
        settings_type = settings_rest.payload["settings_type"]
        settings_value = settings_rest.payload["settings_value"]

        settings = Settings(
            settings_name=settings_name,
            settings_alias=settings_alias.lower(),
            settings_type=settings_type.lower(),
            settings_value=settings_value,
            date_created=datetime.now(),
            date_modified=datetime.now(),
        )

        db.session.add(settings)
        db.session.commit()
        return settings, 201


@settings_rest.route("settings/<string:settings_type>")
class GetSettings(Resource):
    @settings_rest.marshal_with(settings_model)
    def get(self, settings_type):
        return Settings.query.filter_by(settings_type=settings_type).all()


@settings_rest.route("settings/delete/<int:id>")
class DeleteSettings(Resource):
    def delete(self, id):
        Settings.query.filter_by(id=id).delete()
        db.session.commit()

        return "success", 200


@settings_api.before_app_first_request
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
