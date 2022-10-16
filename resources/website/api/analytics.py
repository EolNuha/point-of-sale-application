from datetime import datetime, date, time, timedelta
from flask import Blueprint, request, jsonify, request
from website.models import Sale, Purchase, Product, SaleItem
import sqlalchemy as sa
from decimal import *
from website.helpers import get_change
import pandas as pd
analytics = Blueprint('analytics', __name__)

@analytics.route('/analytics/sales', methods=["GET"])
def getSales():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end = datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)
        
    date_diff = abs((date_start - date_end).days)

    prev_date_start = date_start - timedelta(days=date_diff)
    prev_date_end = datetime.combine((date_start - timedelta(days=1)), time.max)


    curr_sales = Sale.query.filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created >= date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .all()

    prev_sales = Sale.query.filter(Sale.date_created <= prev_date_end)\
        .filter(Sale.date_created >= prev_date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .all()

    sale_analytics = {"options": [], "series": [], "info": {}}
    
    date_ranges = pd.date_range(date_start, date_end)
    date_ranges = [d.strftime("%d/%m/%Y") for d in date_ranges]
    sale_analytics["options"] = date_ranges

    curr_incomp_series = []
    curr_comp_series = [0] * len(sale_analytics["options"])
    curr_options = []
    prev_incomp_series = []
    prev_comp_series = [0] * len(sale_analytics["options"])
    prev_options = []

    for item in curr_sales:
        curr_options.append(item.date_created.strftime('%d/%m/%Y'))
        curr_incomp_series.append(item.total_amount)

    for item in prev_sales:
        option_date = item.date_created + timedelta(date_diff)
        prev_options.append(option_date.strftime('%d/%m/%Y'))
        prev_incomp_series.append(item.total_amount)
    
    for index, d in enumerate(date_ranges):
        if d in curr_options:
            curr_idx = curr_options.index(d)
            curr_comp_series[index] = curr_incomp_series[curr_idx]
        if d in prev_options:
            prev_idx = prev_options.index(d)
            prev_comp_series[index] = prev_incomp_series[prev_idx]

    sale_analytics["series"].append({"name": "Revenue", "data": curr_comp_series})
    if prev_incomp_series:
        sale_analytics["series"].append({"name": "Revenue (previous period)", "data": prev_comp_series})
    currTotal = sum(curr_comp_series)
    prevTotal = sum(prev_comp_series)
    percentage_diff = get_change(Decimal(currTotal), Decimal(prevTotal))
    sale_analytics["info"].update({"chartName": "sales-revenue", "currTotal": currTotal, "prevTotal": prevTotal, "percentageDiff": percentage_diff})
    return jsonify(sale_analytics)


@analytics.route('/analytics/sales/<string:day>', methods=["GET"])
def getSaleStats(day):
    startdate = day.split("-")

    date_start = datetime.combine(date(year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])), time.min)
    date_end = datetime.combine(date(year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])), time.max)
        
    sales = Sale.query.filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created >= date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d-%H-%M", Sale.date_created))\
        .all()

    sale_analytics = {"options": [], "series": [], "info": {}}

    curr_series = []

    for item in sales:
        sale_analytics["options"].append(item.date_created.strftime('%H:%M'))
        curr_series.append(item.total_amount)

    sale_analytics["series"].append({"name": "revenue", "data": curr_series})
    sale_analytics["info"].update({"chartName": f"{day}--sale-revenue"})
    return jsonify(sale_analytics)


@analytics.route('/analytics/purchases', methods=["GET"])
def getPurchases():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end = datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)

    purchases = Purchase.query.filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created >= date_start)\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            sa.func.sum(Purchase.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))\
        .order_by(Purchase.id.desc()).all()

    purchases_analytics = {"options": [], "series": [], "info": {}}
    curr_series = []
    for item in purchases:
        purchases_analytics["options"].append(item.date_created.strftime('%d/%m/%Y'))
        curr_series.append(item.total_amount)

    purchases_analytics["series"].append({"name": "purchase", "data": curr_series})
    purchases_analytics["info"].update({"chartName": "purchases-revenue"})
    return jsonify(purchases_analytics)

@analytics.route('/analytics/purchases/<string:day>', methods=["GET"])
def getPurchaseStats(day):
    startdate = day.split("-")

    date_start = datetime.combine(date(year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])), time.min)
    date_end = datetime.combine(date(year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])), time.max)
        
    purchases = Purchase.query.filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created >= date_start)\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            sa.func.sum(Purchase.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d-%H-%M", Purchase.date_created))\
        .all()

    purchase_analytics = {"options": [], "series": [], "info": {}}

    curr_series = []

    for item in purchases:
        purchase_analytics["options"].append(item.date_created.strftime('%H:%M'))
        curr_series.append(item.total_amount)

    purchase_analytics["series"].append({"name": "purchase", "data": curr_series})
    purchase_analytics["info"].update({"chartName": f"{day}--purchase-revenue"})
    return jsonify(purchase_analytics)

@analytics.route('/analytics/products-sold-by-amount', methods=["GET"])
def getTopProducts():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end = datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)

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

    products_analytics = {"options": [], "series": [], "info": {}}
    curr_series = []

    for item in products:
        products_analytics["options"].append(item.product_name)
        curr_series.append(item.total_amount)

    products_analytics["series"].append({"name": "revenue", "data": curr_series})
    products_analytics["info"].update({"chartName": "top-products-revenue"})
    return jsonify(products_analytics)

@analytics.route('/analytics/products/<int:id>', methods=["GET"])
def getProductStats(id):
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end = datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)

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
        .group_by(sa.func.strftime("%Y-%m-%d", SaleItem.date_created))\
        .order_by(SaleItem.date_created).all()

    products_analytics = {"options": [], "series": [], "info": {}}
    curr_series = []

    for item in products:
        products_analytics["options"].append(item.date_created.strftime('%d/%m/%Y'))
        curr_series.append(item.total_amount)
    
    products_analytics["series"].append({"name": "revenue", "data": curr_series})
    products_analytics["info"].update({"chartName": "product-stats"})

    return jsonify(products_analytics)