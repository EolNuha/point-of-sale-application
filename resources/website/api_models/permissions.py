from flask_restx import fields

from .. import swagger

permissions_model = swagger.model("Permissions", {
    "id": fields.Integer,
    "user_role": fields.String,
    "subject": fields.String,
    "action": fields.String,
    "key": fields.String,
    "date_created": fields.String,
    "date_modified": fields.String,
})

permissions_create_model = swagger.model("PermissionsCreate", {
    "user_role": fields.String,
    "subject": fields.String,
    "action": fields.String,
})

permissions_update_model = swagger.model("PermissionsUpdate", {
    "user_role": fields.String,
    "key": fields.String,
})