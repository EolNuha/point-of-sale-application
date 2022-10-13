from datetime import datetime, date, timedelta, time
from flask import Blueprint, request, jsonify, request
from website.models import Sale, Purchase, Product, SaleItem
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
        sale_analytics["options"].append(item.date_created.strftime('%d/%m/%Y'))
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
        purchases_analytics["options"].append(item.date_created.strftime('%d/%m/%Y'))
        purchases_analytics["series"].append(item.total_amount)

    return jsonify(purchases_analytics)

@analytics.route('/analytics/products-sold-by-amount', methods=["GET"])
def getTopProducts():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end =  datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)

    products = SaleItem.query.filter(SaleItem.date_created <= date_end)\
        .filter(SaleItem.date_created >= date_start)\
        .with_entities(
            SaleItem.id.label("id"), 
            SaleItem.date_created.label("date_created"), 
            SaleItem.product_name.label("product_name"), 
            sa.func.sum(SaleItem.total_amount).label("total_amount"),
        )\
        .group_by(SaleItem.product_name)\
        .order_by(sa.func.sum(SaleItem.total_amount)).limit(10).all()

    products_analytics = {"options": [], "series": []}

    for item in products:
        products_analytics["options"].append(item.product_name)
        products_analytics["series"].append(item.total_amount)

    return jsonify(products_analytics)

@analytics.route('/analytics/products/<int:id>', methods=["GET"])
def getProductStats(id):
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end =  datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)

    products = SaleItem.query.filter(SaleItem.date_created <= date_end)\
        .filter(SaleItem.date_created >= date_start)
    
    if id:
        products = products.filter_by(product_id=id)
    else:
        product = Product.query.order_by(Purchase.id.desc()).all()
        products = products.filter_by(product_id=product.id)
    
    products = products.with_entities(
            SaleItem.id.label("id"), 
            SaleItem.date_created.label("date_created"), 
            sa.func.sum(SaleItem.total_amount).label("total_amount"),
        )\
        .group_by(SaleItem.date_created)\
        .order_by(SaleItem.date_created).all()

    products_analytics = {"options": [], "series": [], "info": []}

    for item in products:
        products_analytics["options"].append(item.date_created.strftime('%d/%m/%Y'))
        products_analytics["series"].append(item.total_amount)

    return jsonify(products_analytics)