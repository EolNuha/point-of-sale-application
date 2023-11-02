from flask_restx import fields

from .. import swagger

notification_model = swagger.model("Notification", {
    "id": fields.Integer,
    "notification_message": fields.String,
    "notification_type": fields.String,
    "notification_read": fields.Boolean,
    "notification_star": fields.Boolean,
    "date_created": fields.String,
    "date_modified": fields.String,
})

notification_input_model = swagger.model("NotificationInput", {
    "star": fields.Boolean,
    "read": fields.Boolean,
})

notifications_input_model = swagger.model("NotificationsInput", {
    "notifications": fields.List(fields.Raw),
})