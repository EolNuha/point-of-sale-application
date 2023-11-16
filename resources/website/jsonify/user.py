def getUserDict(item):
    return {
        "id": item.id,
        "first_name": item.first_name,
        "last_name": item.last_name,
        "username": item.username,
        "user_role": item.user_role,
        "email": item.email,
        "active": item.active,
        "date_created": item.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%d.%m.%Y, %H:%M:%S"),
    }


def getUsersList(users):
    return [getUserDict(i) for i in users]
