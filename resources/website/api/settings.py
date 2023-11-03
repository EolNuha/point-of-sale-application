from website.models.settings import Settings
from datetime import datetime
from website import db
from flask_restx import Resource, Namespace
from website.api_models.settings import settings_model, settings_input_model

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
