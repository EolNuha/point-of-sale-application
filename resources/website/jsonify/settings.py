

def getSettingsDict(item):
    return {
        "id": item.id,
        "settingsName": item.settings_name,
        "settingsAlias": item.settings_alias,
        "settingsType": item.settings_type,
        "settingsValue": item.settings_value,
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getTaxDict(item):
    return {
        "id": item.id,
        "taxName": item.tax_name,
        "taxAlias": item.tax_alias,
        "taxValue": item.tax_value,
    }

def getSettingsList(items):
    return [getSettingsDict(i) for i in items]

def getTaxesList(items):
    return [getTaxDict(i) for i in items]