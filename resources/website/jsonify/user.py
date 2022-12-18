def getUserDict(item):
    return {
        "id": item.id,
        "firstName": item.first_name,
        "lastName": item.last_name,
        "username": item.username,
        "userRole": item.user_role,
        "email": item.email,
        "active": item.active,
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getUsersList(users):
    return [getUserDict(i) for i in users]