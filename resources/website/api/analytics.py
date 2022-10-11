from datetime import datetime, date, timedelta, time
from flask import Blueprint, request, jsonify, request
from website.models import Sale, Purchase
from website.helpers import getPaginatedDict, getSalesList, getSaleItemsList, getDailySalesList
from website import db
from sqlalchemy import or_
import sqlalchemy as sa
from decimal import *
import xlsxwriter
from pathlib import Path
import requests
from website.token import token_required, currentUser

analytics = Blueprint('analytics', __name__)
BASE_URL = "http://localhost:5000"

@analytics.route('/analytics/sales', methods=["GET"])
def getSales():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end =  datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)
        
    sales = Sale.query.filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created >= date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .all()

    sale_analytics = {"options": [], "series": []}

    for item in sales:
        sale_analytics["options"].append(item.date_created.strftime('%m/%d'))
        sale_analytics["series"].append(item.total_amount)

    return jsonify(sale_analytics)


@analytics.route('/analytics/purchases', methods=["GET"])
def getPurchases():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end =  datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)

    purchases = Purchase.query.filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created >= date_start)\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            sa.func.sum(Purchase.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))\
        .order_by(Purchase.id.desc()).all()

    purchases_analytics = {"options": [], "series": []}

    for item in purchases:
        purchases_analytics["options"].append(item.date_created.strftime('%m/%d'))
        purchases_analytics["series"].append(item.total_amount)

    return jsonify(purchases_analytics)