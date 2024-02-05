from flask import current_app, jsonify
from website.models.settings import Settings
from datetime import datetime
from website import db
from flask_restx import Resource, Namespace, reqparse
import werkzeug
from website.api_models.settings import settings_model, settings_input_model
import os
from website.models.settings import Company

settings_rest = Namespace("Settings")

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, default="")
parser.add_argument("address", type=str, default="")
parser.add_argument("phone", type=str, default="")
parser.add_argument("tax_number", type=str, default="")
parser.add_argument("fiscal_number", type=str, default="")
parser.add_argument("logo", type=str, default="")
parser.add_argument(
    "file",
    type=werkzeug.datastructures.FileStorage,
    location="files",
    required=False,
    help="File upload",
)


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


@settings_rest.route("settings/company")
class CompanyDetails(Resource):
    @settings_rest.expect(parser)
    def put(self):
        args = parser.parse_args()
        name = args["name"]
        address = args["address"]
        phone = args["phone"]
        tax_number = args["tax_number"]
        fiscal_number = args["fiscal_number"]
        logo = args["logo"]
        file = args["file"]
        company = Company.query.first()
        if file:
            filename = werkzeug.utils.secure_filename(file.filename)
            _, file_extension = os.path.splitext(filename)
            save_path = os.path.join(
                current_app.static_folder, "", f"companyLogo{file_extension}"
            )
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)
            logo = f"http://localhost:5000/static/companyLogo{file_extension}"

        if company:
            company.name = name
            company.address = address
            company.phone = phone
            company.tax_number = tax_number
            company.fiscal_number = fiscal_number
            company.logo = logo
        else:
            company = Company(
                name=name,
                address=address,
                phone=phone,
                tax_number=tax_number,
                fiscal_number=fiscal_number,
                logo=logo,
            )
            db.session.add(company)
        db.session.commit()

        return "success"

    def get(self):
        company = Company.query.first()
        if not company:
            return jsonify({})
        return jsonify(
            {
                "name": company.name,
                "address": company.address,
                "phone": company.phone,
                "tax_number": company.tax_number,
                "fiscal_number": company.fiscal_number,
                "logo": company.logo,
            }
        )
