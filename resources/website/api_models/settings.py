from flask_restx import fields

from .. import swagger

settings_model = swagger.model("Settings", {
    "id": fields.Integer,
    "settings_name": fields.String,
    "settings_alias": fields.String,
    "settings_type": fields.String,
    "settings_value": fields.String,
    "date_created": fields.String,
    "date_modified": fields.String,
})

settings_input_model = swagger.model("SettingsInput", {
    "settings_name": fields.String,
    "settings_alias": fields.String,
    "settings_type": fields.String,
    "settings_value": fields.String,
})