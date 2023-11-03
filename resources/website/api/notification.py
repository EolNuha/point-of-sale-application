from website.models.notification import Notification
from website.jsonify.notification import getNotificationList
from website.helpers import get_page_range
from website import db
from sqlalchemy import asc, desc
from flask_restx import Resource, Namespace, reqparse
from website.api_models.notification import (
    notifications_input_model,
    notification_input_model,
)
from website.api_models.pagination import pagination

notification_rest = Namespace("Notification")
parser = reqparse.RequestParser()
parser.add_argument("page", type=int, default=1)
parser.add_argument("per_page", type=int, default=5)
parser.add_argument("col_name", type=str)
parser.add_argument("sort_column", type=str, default="date_created")
parser.add_argument("sort_dir", type=str, default="desc")


@notification_rest.route("notifications")
class Notifications(Resource):
    @notification_rest.doc(
        params={
            "page": "",
            "per_page": "",
            "col_name": "",
            "sort_column": "",
            "sort_dir": "",
        }
    )
    @notification_rest.marshal_with(pagination)
    def get(self):
        args = parser.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        col_name = args["col_name"]
        sort_column = args["sort_column"]
        sort_dir = args["sort_dir"]

        sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

        query = Notification.query.order_by(sort)

        if col_name == "read":
            query = query.filter_by(notification_read=False)
        elif col_name == "star":
            query = query.filter_by(notification_star=True)

        paginated_items = query.paginate(page=page, per_page=per_page)
        response = {
            "has_next": paginated_items.has_next,
            "has_prev": paginated_items.has_prev,
            "page": paginated_items.page,
            "per_page": paginated_items.per_page,
            "pages": paginated_items.pages,
            "next_num": paginated_items.next_num,
            "prev_num": paginated_items.prev_num,
            "data": getNotificationList(paginated_items.items),
            "items": len(paginated_items.items),
            "total": paginated_items.total,
            "page_range": get_page_range(paginated_items.page, paginated_items.pages),
        }
        return response

    @notification_rest.expect(notifications_input_model)
    def put(self):
        notifications = notification_rest.payload["notifications"]
        for item in notifications:
            notification_record = Notification.query.filter_by(id=item["id"]).first()
            notification_record.notification_read = item["read"]
            notification_record.notification_star = item["star"]
            db.session.commit()

        return "success", 200

    @notification_rest.expect(notifications_input_model)
    def delete(self):
        notifications = notification_rest.payload["notifications"]
        for item in notifications:
            Notification.query.filter_by(id=item["id"]).delete()
            db.session.commit()
        return "success", 200


@notification_rest.route("notifications/<int:id>")
class NotificationItem(Resource):
    @notification_rest.expect(notification_input_model)
    def put(self, id):
        read = notification_rest.payload["read"]
        star = notification_rest.payload["star"]

        notification_info = Notification.query.filter_by(id=id).first()
        if read != None:
            notification_info.notification_read = read
        if star != None:
            notification_info.notification_star = star
        db.session.commit()
        return "Success", 200

    def delete(self, id):
        Notification.query.filter_by(id=id).delete()
        db.session.commit()
        return "success", 200
