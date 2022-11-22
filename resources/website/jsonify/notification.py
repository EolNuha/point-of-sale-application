from datetime import datetime

def getNotificationDict(item):
    return {
        "id": item.id,
        "toId": item.notification_to_id,
        "message": item.notification_message,
        "type": item.notification_type,
        "read": item.notification_read,
        "star": item.notification_star,
        "dateCreated": datetime.strptime(item.date_created.strftime('%d.%m.%Y %H:%M:%S,%f'),'%d.%m.%Y %H:%M:%S,%f').timestamp() * 1000,
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getNotificationList(items):
    return [getNotificationDict(i) for i in items]