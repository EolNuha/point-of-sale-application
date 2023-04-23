from flask import Blueprint, request, jsonify, request
from website.models.settings import Settings
from website.jsonify.settings import getSettingsList
from datetime import datetime
from website import db

settings_api = Blueprint('settings_api', __name__)

@settings_api.route('/settings', methods=["POST"])
def createSettings():
    settings_name = request.json["settingsName"]
    settings_alias = request.json["settingsAlias"]
    settings_type = request.json["settingsType"]
    settings_value = request.json["settingsValue"]

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
    data = {
        "settingsId": settings.id 
    }
    return jsonify(data), 200

@settings_api.route('/settings/<string:settings_type>', methods=["GET"])
def getSettings(settings_type):
    items = Settings.query.filter_by(settings_type=settings_type).all()
    return jsonify(getSettingsList(items))

@settings_api.route('/settings/delete/<int:id>', methods=["GET"])
def deleteSettings(id):
    Settings.query.filter_by(id=id).delete()
    db.session.commit()
    
    return "success",200

@settings_api.before_app_first_request
def createDemoSettings():
    if(Settings.query.count() > 0):
        return
    demo = [
        ["storage", "storage", "notification", 1500],
        ["pcs", "pcs", "measure", "pcs"],
        ["kg", "kg", "measure", "kg"],
        ["liter", "liter", "measure", "liter"],
        ["purchase", "purchase", "purchasetype", "purchase"],
        ["investment", "investment", "purchasetype", "investment"],
        ["expense", "expense", "purchasetype", "expense"],
        ["8", "eight", "tax", 8],
        ["18", "eighteen", "tax", 18],
    ]
    for i in demo:
        db.session.add(Settings(
            settings_name=i[0],
            settings_alias=i[1],
            settings_type=i[2],
            settings_value=i[3],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            ))
        db.session.commit()
    return "success", 200