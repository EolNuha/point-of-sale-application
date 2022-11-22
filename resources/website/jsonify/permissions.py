def getPermissionsDict(item):
    return {
        "id": item.id,
        "subject": item.subject,
        "action": item.action,
        "key": item.key,
    }

def getPermissionsList(items):
    return [getPermissionsDict(i) for i in items]