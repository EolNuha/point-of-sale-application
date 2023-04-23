from datetime import datetime, date, time
from flask import Blueprint, request, jsonify, request
from website.models.sale import Sale, SaleItem
from website.models.purchase import Purchase
from website.models.user import User
import sqlalchemy as sa
from decimal import *
from website.helpers import get_percentage_change, get_curr_prev_chart, get_curr_prev_dates
from website.token import currentUser
import decimal

analytics_api = Blueprint('analytics_api', __name__)
Decimal = decimal.Decimal
TWOPLACES = Decimal(10) ** -2

@analytics_api.route('/analytics/sales', methods=["GET"])
def getSales():
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]
    prev_date_start = request_dates["prev_date_start"]
    prev_date_end = request_dates["prev_date_end"]

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
    
    dates = get_curr_prev_chart(date_start, date_end, curr_sales, prev_sales)
    
    curr_comp_series = dates["curr_series"]
    prev_comp_series = dates["prev_series"]
    sale_analytics["options"] = dates["options"]
    curr_total = sum(curr_comp_series)
    prev_total = sum(prev_comp_series)

    sale_analytics["series"].append({"name": "revenue", "data": curr_comp_series})
    sale_analytics["series"].append({"name": "revenuePreviousPeriod", "data": prev_comp_series})
    
    percentage_diff = get_percentage_change(Decimal(curr_total), Decimal(prev_total))
    sale_analytics["info"].update({
        "chartName": "sales-revenue", 
        "currTotal": curr_total, 
        "prevTotal": prev_total, 
        "percentageDiff": percentage_diff
    })
    return jsonify(sale_analytics)

@analytics_api.route('/analytics/sales-gross-profit', methods=["GET"])
def getSalesGrossProfit():
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]
    prev_date_start = request_dates["prev_date_start"]
    prev_date_end = request_dates["prev_date_end"]

    curr_sales = Sale.query.filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created >= date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.gross_profit_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .all()

    prev_sales = Sale.query.filter(Sale.date_created <= prev_date_end)\
        .filter(Sale.date_created >= prev_date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.gross_profit_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .all()

    sale_analytics = {"options": [], "series": [], "info": {}}
    
    dates = get_curr_prev_chart(date_start, date_end, curr_sales, prev_sales)
    
    curr_comp_series = dates["curr_series"]
    prev_comp_series = dates["prev_series"]
    sale_analytics["options"] = dates["options"]
    curr_total = sum(curr_comp_series)
    prev_total = sum(prev_comp_series)

    sale_analytics["series"].append({"name": "grossProfit", "data": curr_comp_series})
    sale_analytics["series"].append({"name": "grossProfitPreviousPeriod", "data": prev_comp_series})
    
    percentage_diff = get_percentage_change(Decimal(curr_total), Decimal(prev_total))
    sale_analytics["info"].update({
        "chartName": "sales-revenue", 
        "currTotal": curr_total, 
        "prevTotal": prev_total, 
        "percentageDiff": percentage_diff
    })
    return jsonify(sale_analytics)


@analytics_api.route('/analytics/sales/<string:day>', methods=["GET"])
def getSaleStats(day):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    startdate = day.split("-")

    date_start = datetime.combine(date(year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])), time.min)
    date_end = datetime.combine(date(year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])), time.max)
        
    sales = Sale.query.filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created >= date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.total_amount).label("total_amount"),
            sa.func.sum(Sale.gross_profit_amount).label("gross_profit_amount"),
            sa.func.sum(Sale.net_profit_amount).label("net_profit_amount"),
        )\
        .group_by(sa.func.strftime("%H-%M", Sale.date_created))\
        .all()

    sale_analytics = {"options": [], "series": [], "info": {}}

    curr_series = []
    gross_series = []
    net_series = []

    for item in sales:
        sale_analytics["options"].append(item.date_created.strftime('%H:%M'))
        curr_series.append(Decimal(item.total_amount).quantize(TWOPLACES))
        gross_series.append(Decimal(item.gross_profit_amount).quantize(TWOPLACES))
        net_series.append(Decimal(item.net_profit_amount).quantize(TWOPLACES))

    sale_analytics["series"].append({"name": "revenue", "data": curr_series})
    sale_analytics["series"].append({"name": "grossProfit", "data": gross_series})
    sale_analytics["series"].append({"name": "netProfit", "data": net_series})
    sale_analytics["info"].update({"chartName": f"{day}--sale-revenue", "currTotal": sum(curr_series), "grossTotal": sum(gross_series), "netTotal": sum(net_series)})
    return jsonify(sale_analytics)


@analytics_api.route('/analytics/purchases', methods=["GET"])
def getPurchases():
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]
    prev_date_start = request_dates["prev_date_start"]
    prev_date_end = request_dates["prev_date_end"]

    curr_purchases = Purchase.query.filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created >= date_start)\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            sa.func.sum(Purchase.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))\
        .order_by(Purchase.id.desc()).all()

    prev_purchases = Purchase.query.filter(Purchase.date_created <= prev_date_end)\
        .filter(Purchase.date_created >= prev_date_start)\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            sa.func.sum(Purchase.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))\
        .order_by(Purchase.id.desc()).all()

    purchases_analytics = {"options": [], "series": [], "info": {}}
    
    dates = get_curr_prev_chart(date_start, date_end, curr_purchases, prev_purchases)
    
    curr_comp_series = dates["curr_series"]
    prev_comp_series = dates["prev_series"]
    purchases_analytics["options"] = dates["options"]
    curr_total = sum(curr_comp_series)
    prev_total = sum(prev_comp_series)

    purchases_analytics["series"].append({"name": "purchase", "data": curr_comp_series})
    purchases_analytics["series"].append({"name": "purchasePreviousPeriod", "data": prev_comp_series})
    
    percentage_diff = get_percentage_change(Decimal(curr_total), Decimal(prev_total))
    purchases_analytics["info"].update({
        "chartName": "purchases-revenue", 
        "currTotal": curr_total, 
        "prevTotal": prev_total, 
        "percentageDiff": percentage_diff
    })
    return jsonify(purchases_analytics)

@analytics_api.route('/analytics/purchases/<string:day>', methods=["GET"])
def getPurchaseStats(day):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
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
        curr_series.append(Decimal(item.total_amount).quantize(TWOPLACES))

    purchase_analytics["series"].append({"name": "purchase", "data": curr_series})
    purchase_analytics["info"].update({"chartName": f"{day}--purchase-revenue", "currTotal": sum(curr_series)})
    return jsonify(purchase_analytics)

@analytics_api.route('/analytics/sellers/<string:name>', methods=["GET"])
def getSellerStats(name):
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]
    prev_date_start = request_dates["prev_date_start"]
    prev_date_end = request_dates["prev_date_end"]   

    curr_purchases = Purchase.query.filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created >= date_start)

    prev_purchases = Purchase.query.filter(Purchase.date_created <= prev_date_end)\
        .filter(Purchase.date_created >= prev_date_start)
    
    if name and name != 'null':
        curr_purchases = curr_purchases.filter_by(seller_name=name)
        prev_purchases = prev_purchases.filter_by(seller_name=name)
    else:
        return "Not Found", 404
    
    curr_purchases = curr_purchases.with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            sa.func.sum(Purchase.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))\
        .order_by(Purchase.date_created).all()
    
    prev_purchases = prev_purchases.with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            sa.func.sum(Purchase.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))\
        .order_by(Purchase.date_created).all()

    seller_analytics = {"options": [], "series": [], "info": {}}

    dates = get_curr_prev_chart(date_start, date_end, curr_purchases, prev_purchases)
    
    curr_comp_series = dates["curr_series"]
    prev_comp_series = dates["prev_series"]
    seller_analytics["options"] = dates["options"]
    curr_total = sum(curr_comp_series)
    prev_total = sum(prev_comp_series)

    seller_analytics["series"].append({"name": "purchase", "data": curr_comp_series})
    seller_analytics["series"].append({"name": "purchasePreviousPeriod", "data": prev_comp_series})
    
    percentage_diff = get_percentage_change(Decimal(curr_total), Decimal(prev_total))
    seller_analytics["info"].update({
        "chartName": "seller-stats", 
        "currTotal": curr_total, 
        "prevTotal": prev_total, 
        "percentageDiff": percentage_diff
    })
    return jsonify(seller_analytics)

@analytics_api.route('/analytics/products-sold-by-amount', methods=["GET"])
def getTopProducts():
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]

    products = SaleItem.query.filter(SaleItem.date_created <= date_end)\
        .filter(SaleItem.date_created >= date_start)\
        .with_entities(
            SaleItem.id.label("id"), 
            SaleItem.date_created.label("date_created"), 
            SaleItem.product_name.label("product_name"), 
            sa.func.sum(SaleItem.total_amount).label("total_amount"),
        )\
        .group_by(SaleItem.product_name)\
        .order_by(sa.func.sum(SaleItem.total_amount).desc()).limit(10).all()

    products_analytics = {"options": [], "series": [], "info": {}}
    curr_series = []

    for item in products:
        products_analytics["options"].append(item.product_name)
        curr_series.append(Decimal(item.total_amount).quantize(TWOPLACES))

    products_analytics["series"].append({"name": "revenue", "data": curr_series})
    products_analytics["info"].update({"chartName": "top-products-revenue", "currTotal": sum(curr_series)})
    return jsonify(products_analytics)


@analytics_api.route('/analytics/products-sold-by-gross-profit', methods=["GET"])
def getTopProductsByGrossProfit():
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]

    products = SaleItem.query.filter(SaleItem.date_created <= date_end)\
        .filter(SaleItem.date_created >= date_start)\
        .with_entities(
            SaleItem.id.label("id"), 
            SaleItem.date_created.label("date_created"), 
            SaleItem.product_name.label("product_name"), 
            sa.func.sum(SaleItem.gross_profit_amount).label("gross_profit_amount"),
        )\
        .group_by(SaleItem.product_name)\
        .order_by(sa.func.sum(SaleItem.gross_profit_amount).desc()).limit(10).all()

    products_analytics = {"options": [], "series": [], "info": {}}
    curr_series = []

    for item in products:
        products_analytics["options"].append(item.product_name)
        curr_series.append(Decimal(item.gross_profit_amount).quantize(TWOPLACES))

    products_analytics["series"].append({"name": "revenue", "data": curr_series})
    products_analytics["info"].update({"chartName": "top-products-revenue", "currTotal": sum(curr_series)})
    return jsonify(products_analytics)

@analytics_api.route('/analytics/products-sold-by-net-profit', methods=["GET"])
def getTopProductsByNetProfit():
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]

    products = SaleItem.query.filter(SaleItem.date_created <= date_end)\
        .filter(SaleItem.date_created >= date_start)\
        .with_entities(
            SaleItem.id.label("id"), 
            SaleItem.date_created.label("date_created"), 
            SaleItem.product_name.label("product_name"), 
            sa.func.sum(SaleItem.net_profit_amount).label("net_profit_amount"),
        )\
        .group_by(SaleItem.product_name)\
        .order_by(sa.func.sum(SaleItem.net_profit_amount).desc()).limit(10).all()

    products_analytics = {"options": [], "series": [], "info": {}}
    curr_series = []

    for item in products:
        products_analytics["options"].append(item.product_name)
        curr_series.append(Decimal(item.net_profit_amount).quantize(TWOPLACES))

    products_analytics["series"].append({"name": "revenue", "data": curr_series})
    products_analytics["info"].update({"chartName": "top-products-revenue", "currTotal": sum(curr_series)})
    return jsonify(products_analytics)

@analytics_api.route('/analytics/products/<int:id>', methods=["GET"])
def getProductStats(id):
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]
    prev_date_start = request_dates["prev_date_start"]
    prev_date_end = request_dates["prev_date_end"]   

    curr_products = SaleItem.query.filter(SaleItem.date_created <= date_end)\
        .filter(SaleItem.date_created >= date_start)

    prev_products = SaleItem.query.filter(SaleItem.date_created <= prev_date_end)\
        .filter(SaleItem.date_created >= prev_date_start)
    
    if id:
        curr_products = curr_products.filter_by(product_id=id)
        prev_products = prev_products.filter_by(product_id=id)
    else:
        return "Not Found", 404
    
    curr_products = curr_products.with_entities(
            SaleItem.id.label("id"), 
            SaleItem.date_created.label("date_created"), 
            sa.func.sum(SaleItem.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", SaleItem.date_created))\
        .order_by(SaleItem.date_created).all()
    
    prev_products = prev_products.with_entities(
            SaleItem.id.label("id"), 
            SaleItem.date_created.label("date_created"), 
            sa.func.sum(SaleItem.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", SaleItem.date_created))\
        .order_by(SaleItem.date_created).all()

    products_analytics = {"options": [], "series": [], "info": {}}

    dates = get_curr_prev_chart(date_start, date_end, curr_products, prev_products)
    
    curr_comp_series = dates["curr_series"]
    prev_comp_series = dates["prev_series"]
    products_analytics["options"] = dates["options"]
    curr_total = sum(curr_comp_series)
    prev_total = sum(prev_comp_series)

    products_analytics["series"].append({"name": "revenue", "data": curr_comp_series})
    products_analytics["series"].append({"name": "revenuePreviousPeriod", "data": prev_comp_series})
    
    percentage_diff = get_percentage_change(Decimal(curr_total), Decimal(prev_total))
    products_analytics["info"].update({
        "chartName": "product-stats", 
        "currTotal": curr_total, 
        "prevTotal": prev_total, 
        "percentageDiff": percentage_diff
    })
    return jsonify(products_analytics)


@analytics_api.route('/analytics/users-revenue', methods=["GET"])
def getTopUsers():
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]

    users = Sale.query.filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created >= date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            Sale.user_id.label("user_id"), 
            sa.func.sum(Sale.total_amount).label("total_amount"),
        )\
        .group_by(Sale.user_id)\
        .order_by(sa.func.sum(Sale.total_amount)).limit(10).all()

    users_analytics = {"options": [], "series": [], "info": {}}
    curr_series = []

    for item in users:
        user = User.query.filter_by(id=item.user_id).first()
        users_analytics["options"].append(user.first_name + ' ' + user.last_name)
        curr_series.append(item.total_amount)

    users_analytics["series"].append({"name": "revenue", "data": curr_series})
    users_analytics["info"].update({"chartName": "top-users-revenue", "currTotal": sum(curr_series)})
    return jsonify(users_analytics)

@analytics_api.route('/analytics/users/<int:id>', methods=["GET"])
def getUserStats(id):
    request_dates = get_curr_prev_dates(request)
    date_start = request_dates["date_start"]
    date_end = request_dates["date_end"]
    prev_date_start = request_dates["prev_date_start"]
    prev_date_end = request_dates["prev_date_end"]

    curr_user_analytics = Sale.query.filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created >= date_start)

    prev_user_analytics = Sale.query.filter(Sale.date_created <= prev_date_end)\
        .filter(Sale.date_created >= prev_date_start)
    
    if id:
        curr_user_analytics = curr_user_analytics.filter_by(user_id=id)
        prev_user_analytics = prev_user_analytics.filter_by(user_id=id)
    else:
        logged_in_user = currentUser(request)
        curr_user_analytics = curr_user_analytics.filter_by(user_id=logged_in_user.id)
        prev_user_analytics = prev_user_analytics.filter_by(user_id=logged_in_user.id)
    
    curr_user_analytics = curr_user_analytics.with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .order_by(Sale.date_created).all()
    
    prev_user_analytics = prev_user_analytics.with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            sa.func.sum(Sale.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .order_by(Sale.date_created).all()

    user_analytics = {"options": [], "series": [], "info": {}}

    dates = get_curr_prev_chart(date_start, date_end, curr_user_analytics, prev_user_analytics)
    
    curr_comp_series = dates["curr_series"]
    prev_comp_series = dates["prev_series"]
    user_analytics["options"] = dates["options"]
    curr_total = sum(curr_comp_series)
    prev_total = sum(prev_comp_series)

    user_analytics["series"].append({"name": "revenue", "data": curr_comp_series})
    user_analytics["series"].append({"name": "revenuePreviousPeriod", "data": prev_comp_series})
    
    percentage_diff = get_percentage_change(Decimal(curr_total), Decimal(prev_total))
    user_analytics["info"].update({
        "chartName": "product-stats", 
        "currTotal": curr_total, 
        "prevTotal": prev_total, 
        "percentageDiff": percentage_diff
    })
    return jsonify(user_analytics)