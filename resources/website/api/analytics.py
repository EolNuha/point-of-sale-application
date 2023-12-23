from datetime import datetime, date, time
from flask import request, jsonify
from website.models.sale import Sale, SaleItem
from website.models.purchase import Purchase
from website.models.user import User
import sqlalchemy as sa
from decimal import *
from website.helpers import (
    get_percentage_change,
    get_curr_prev_chart,
    get_curr_prev_dates,
)
from website.token import currentUser
import decimal
from website.api_models.analytics import percentage_model, gross_net_model, chart_model
from flask_restx import Namespace, Resource, reqparse
from werkzeug.exceptions import NotFound
from website import db
import pandas as pd

analytics_rest = Namespace("Analytics")

Decimal = decimal.Decimal
TWOPLACES = Decimal(10) ** -2
parser = reqparse.RequestParser()
parser.add_argument("start_date", type=str)
parser.add_argument("end_date", type=str)


@analytics_rest.route("analytics/sales")
class GetSales(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(percentage_model)
    def get(self):
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]
        prev_date_start = request_dates["prev_date_start"]
        prev_date_end = request_dates["prev_date_end"]

        curr_sales = (
            Sale.query.filter(Sale.date_created <= date_end)
            .filter(Sale.date_created >= date_start)
            .with_entities(
                Sale.id.label("id"),
                Sale.date_created.label("date_created"),
                sa.func.sum(Sale.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))
            .all()
        )

        prev_sales = (
            Sale.query.filter(Sale.date_created <= prev_date_end)
            .filter(Sale.date_created >= prev_date_start)
            .with_entities(
                Sale.id.label("id"),
                Sale.date_created.label("date_created"),
                sa.func.sum(Sale.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))
            .all()
        )

        sale_analytics = {"options": [], "series": [], "info": {}}

        dates = get_curr_prev_chart(date_start, date_end, curr_sales, prev_sales)

        curr_comp_series = dates["curr_series"]
        prev_comp_series = dates["prev_series"]
        sale_analytics["options"] = dates["options"]
        curr_total = sum(curr_comp_series)
        prev_total = sum(prev_comp_series)

        sale_analytics["series"].append({"name": "revenue", "data": curr_comp_series})
        sale_analytics["series"].append(
            {"name": "revenuePreviousPeriod", "data": prev_comp_series}
        )

        percentage_diff = get_percentage_change(
            Decimal(curr_total), Decimal(prev_total)
        )
        sale_analytics["info"].update(
            {
                "chartName": "sales-revenue",
                "currTotal": curr_total,
                "prevTotal": prev_total,
                "percentageDiff": percentage_diff,
            }
        )
        return sale_analytics


@analytics_rest.route("analytics/sales-gross-profit")
class GetSalesGrossProfit(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(percentage_model)
    def get(self):
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]
        prev_date_start = request_dates["prev_date_start"]
        prev_date_end = request_dates["prev_date_end"]

        curr_sales = (
            Sale.query.filter(Sale.date_created <= date_end)
            .filter(Sale.date_created >= date_start)
            .with_entities(
                Sale.id.label("id"),
                Sale.date_created.label("date_created"),
                sa.func.sum(Sale.gross_profit_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))
            .all()
        )

        prev_sales = (
            Sale.query.filter(Sale.date_created <= prev_date_end)
            .filter(Sale.date_created >= prev_date_start)
            .with_entities(
                Sale.id.label("id"),
                Sale.date_created.label("date_created"),
                sa.func.sum(Sale.gross_profit_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))
            .all()
        )

        sale_analytics = {"options": [], "series": [], "info": {}}

        dates = get_curr_prev_chart(date_start, date_end, curr_sales, prev_sales)

        curr_comp_series = dates["curr_series"]
        prev_comp_series = dates["prev_series"]
        sale_analytics["options"] = dates["options"]
        curr_total = sum(curr_comp_series)
        prev_total = sum(prev_comp_series)

        sale_analytics["series"].append(
            {"name": "grossProfit", "data": curr_comp_series}
        )
        sale_analytics["series"].append(
            {"name": "grossProfitPreviousPeriod", "data": prev_comp_series}
        )

        percentage_diff = get_percentage_change(
            Decimal(curr_total), Decimal(prev_total)
        )
        sale_analytics["info"].update(
            {
                "chartName": "sales-revenue",
                "currTotal": curr_total,
                "prevTotal": prev_total,
                "percentageDiff": percentage_diff,
            }
        )
        return sale_analytics


@analytics_rest.route("analytics/sales/<string:day>")
class GetSaleStats(Resource):
    @analytics_rest.marshal_with(gross_net_model)
    def get(self, day):
        ctx = decimal.getcontext()
        ctx.rounding = decimal.ROUND_HALF_UP
        startdate = day.split("-")

        date_start = datetime.combine(
            date(
                year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])
            ),
            time.min,
        )
        date_end = datetime.combine(
            date(
                year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])
            ),
            time.max,
        )

        sales = (
            Sale.query.filter(Sale.date_created <= date_end)
            .filter(Sale.date_created >= date_start)
            .with_entities(
                Sale.id.label("id"),
                Sale.date_created.label("date_created"),
                sa.func.sum(Sale.total_amount).label("total_amount"),
                sa.func.sum(Sale.gross_profit_amount).label("gross_profit_amount"),
                sa.func.sum(Sale.net_profit_amount).label("net_profit_amount"),
            )
            .group_by(sa.func.strftime("%H-%M", Sale.date_created))
            .all()
        )

        sale_analytics = {"options": [], "series": [], "info": {}}

        curr_series = []
        gross_series = []
        net_series = []

        for item in sales:
            sale_analytics["options"].append(item.date_created.strftime("%H:%M"))
            curr_series.append(Decimal(item.total_amount).quantize(TWOPLACES))
            gross_series.append(Decimal(item.gross_profit_amount).quantize(TWOPLACES))
            net_series.append(Decimal(item.net_profit_amount).quantize(TWOPLACES))

        sale_analytics["series"].append({"name": "revenue", "data": curr_series})
        sale_analytics["series"].append({"name": "grossProfit", "data": gross_series})
        sale_analytics["series"].append({"name": "netProfit", "data": net_series})
        sale_analytics["info"].update(
            {
                "chartName": f"{day}--sale-revenue",
                "currTotal": sum(curr_series),
                "grossTotal": sum(gross_series),
                "netTotal": sum(net_series),
            }
        )
        return sale_analytics


@analytics_rest.route("analytics/purchases")
class GetPurchases(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(percentage_model)
    def get(self):
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]
        prev_date_start = request_dates["prev_date_start"]
        prev_date_end = request_dates["prev_date_end"]

        curr_purchases = (
            Purchase.query.filter(Purchase.date_created <= date_end)
            .filter(Purchase.date_created >= date_start)
            .with_entities(
                Purchase.id.label("id"),
                Purchase.date_created.label("date_created"),
                sa.func.sum(Purchase.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))
            .order_by(Purchase.id.desc())
            .all()
        )

        prev_purchases = (
            Purchase.query.filter(Purchase.date_created <= prev_date_end)
            .filter(Purchase.date_created >= prev_date_start)
            .with_entities(
                Purchase.id.label("id"),
                Purchase.date_created.label("date_created"),
                sa.func.sum(Purchase.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))
            .order_by(Purchase.id.desc())
            .all()
        )

        purchases_analytics = {"options": [], "series": [], "info": {}}

        dates = get_curr_prev_chart(
            date_start, date_end, curr_purchases, prev_purchases
        )

        curr_comp_series = dates["curr_series"]
        prev_comp_series = dates["prev_series"]
        purchases_analytics["options"] = dates["options"]
        curr_total = sum(curr_comp_series)
        prev_total = sum(prev_comp_series)

        purchases_analytics["series"].append(
            {"name": "purchase", "data": curr_comp_series}
        )
        purchases_analytics["series"].append(
            {"name": "purchasePreviousPeriod", "data": prev_comp_series}
        )
        percentage_diff = get_percentage_change(
            Decimal(curr_total), Decimal(prev_total)
        )
        purchases_analytics["info"].update(
            {
                "chartName": "purchases-revenue",
                "currTotal": curr_total,
                "prevTotal": prev_total,
                "percentageDiff": percentage_diff,
            }
        )
        return purchases_analytics


@analytics_rest.route("analytics/purchases/<string:day>")
class GetPurchaseStats(Resource):
    @analytics_rest.marshal_with(chart_model)
    def get(self, day):
        ctx = decimal.getcontext()
        ctx.rounding = decimal.ROUND_HALF_UP
        startdate = day.split("-")

        date_start = datetime.combine(
            date(
                year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])
            ),
            time.min,
        )
        date_end = datetime.combine(
            date(
                year=int(startdate[0]), month=int(startdate[1]), day=int(startdate[2])
            ),
            time.max,
        )

        purchases = (
            Purchase.query.filter(Purchase.date_created <= date_end)
            .filter(Purchase.date_created >= date_start)
            .with_entities(
                Purchase.id.label("id"),
                Purchase.date_created.label("date_created"),
                sa.func.sum(Purchase.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d-%H-%M", Purchase.date_created))
            .all()
        )

        purchase_analytics = {"options": [], "series": [], "info": {}}

        curr_series = []

        for item in purchases:
            purchase_analytics["options"].append(item.date_created.strftime("%H:%M"))
            curr_series.append(Decimal(item.total_amount).quantize(TWOPLACES))

        purchase_analytics["series"].append({"name": "purchase", "data": curr_series})
        purchase_analytics["info"].update(
            {"chartName": f"{day}--purchase-revenue", "currTotal": sum(curr_series)}
        )
        return purchase_analytics


@analytics_rest.route("analytics/sellers/<string:name>")
class GetSellerStats(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(percentage_model)
    def get(self, name):
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]
        prev_date_start = request_dates["prev_date_start"]
        prev_date_end = request_dates["prev_date_end"]

        curr_purchases = Purchase.query.filter(
            Purchase.date_created <= date_end
        ).filter(Purchase.date_created >= date_start)

        prev_purchases = Purchase.query.filter(
            Purchase.date_created <= prev_date_end
        ).filter(Purchase.date_created >= prev_date_start)

        if name and name != "null":
            curr_purchases = curr_purchases.filter_by(seller_name=name)
            prev_purchases = prev_purchases.filter_by(seller_name=name)
        else:
            raise NotFound("Seller was not found!")

        curr_purchases = (
            curr_purchases.with_entities(
                Purchase.id.label("id"),
                Purchase.date_created.label("date_created"),
                sa.func.sum(Purchase.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))
            .order_by(Purchase.date_created)
            .all()
        )

        prev_purchases = (
            prev_purchases.with_entities(
                Purchase.id.label("id"),
                Purchase.date_created.label("date_created"),
                sa.func.sum(Purchase.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))
            .order_by(Purchase.date_created)
            .all()
        )

        seller_analytics = {"options": [], "series": [], "info": {}}

        dates = get_curr_prev_chart(
            date_start, date_end, curr_purchases, prev_purchases
        )

        curr_comp_series = dates["curr_series"]
        prev_comp_series = dates["prev_series"]
        seller_analytics["options"] = dates["options"]
        curr_total = sum(curr_comp_series)
        prev_total = sum(prev_comp_series)

        seller_analytics["series"].append(
            {"name": "purchase", "data": curr_comp_series}
        )
        seller_analytics["series"].append(
            {"name": "purchasePreviousPeriod", "data": prev_comp_series}
        )

        percentage_diff = get_percentage_change(
            Decimal(curr_total), Decimal(prev_total)
        )
        seller_analytics["info"].update(
            {
                "chartName": "seller-stats",
                "currTotal": curr_total,
                "prevTotal": prev_total,
                "percentageDiff": percentage_diff,
            }
        )
        return seller_analytics


@analytics_rest.route("analytics/products-sold-by-amount")
class GetProductsSoldByAmount(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(chart_model)
    def get(self):
        ctx = decimal.getcontext()
        ctx.rounding = decimal.ROUND_HALF_UP
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]

        products = (
            SaleItem.query.filter(SaleItem.date_created <= date_end)
            .filter(SaleItem.date_created >= date_start)
            .with_entities(
                SaleItem.id.label("id"),
                SaleItem.date_created.label("date_created"),
                SaleItem.product_name.label("product_name"),
                sa.func.sum(SaleItem.total_amount).label("total_amount"),
            )
            .group_by(SaleItem.product_name)
            .order_by(sa.func.sum(SaleItem.total_amount).desc())
            .limit(10)
            .all()
        )

        products_analytics = {"options": [], "series": [], "info": {}}
        curr_series = []

        for item in products:
            products_analytics["options"].append(item.product_name)
            curr_series.append(Decimal(item.total_amount).quantize(TWOPLACES))

        products_analytics["series"].append({"name": "revenue", "data": curr_series})
        products_analytics["info"].update(
            {"chartName": "top-products-revenue", "currTotal": sum(curr_series)}
        )
        return products_analytics


@analytics_rest.route("analytics/products-sold-by-gross-profit")
class GetProductsSoldByGrossProfit(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(chart_model)
    def get(self):
        ctx = decimal.getcontext()
        ctx.rounding = decimal.ROUND_HALF_UP
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]

        products = (
            SaleItem.query.filter(SaleItem.date_created <= date_end)
            .filter(SaleItem.date_created >= date_start)
            .with_entities(
                SaleItem.id.label("id"),
                SaleItem.date_created.label("date_created"),
                SaleItem.product_name.label("product_name"),
                sa.func.sum(SaleItem.gross_profit_amount).label("gross_profit_amount"),
            )
            .group_by(SaleItem.product_name)
            .order_by(sa.func.sum(SaleItem.gross_profit_amount).desc())
            .limit(10)
            .all()
        )

        products_analytics = {"options": [], "series": [], "info": {}}
        curr_series = []

        for item in products:
            products_analytics["options"].append(item.product_name)
            curr_series.append(Decimal(item.gross_profit_amount).quantize(TWOPLACES))

        products_analytics["series"].append({"name": "revenue", "data": curr_series})
        products_analytics["info"].update(
            {"chartName": "top-products-revenue", "currTotal": sum(curr_series)}
        )
        return products_analytics


@analytics_rest.route("analytics/products-sold-by-gross-profit")
class GetProductsSoldByGrossProfit(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(chart_model)
    def get(self):
        ctx = decimal.getcontext()
        ctx.rounding = decimal.ROUND_HALF_UP
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]

        products = (
            SaleItem.query.filter(SaleItem.date_created <= date_end)
            .filter(SaleItem.date_created >= date_start)
            .with_entities(
                SaleItem.id.label("id"),
                SaleItem.date_created.label("date_created"),
                SaleItem.product_name.label("product_name"),
                sa.func.sum(SaleItem.gross_profit_amount).label("gross_profit_amount"),
            )
            .group_by(SaleItem.product_name)
            .order_by(sa.func.sum(SaleItem.gross_profit_amount).desc())
            .limit(10)
            .all()
        )

        products_analytics = {"options": [], "series": [], "info": {}}
        curr_series = []

        for item in products:
            products_analytics["options"].append(item.product_name)
            curr_series.append(Decimal(item.gross_profit_amount).quantize(TWOPLACES))

        products_analytics["series"].append({"name": "revenue", "data": curr_series})
        products_analytics["info"].update(
            {"chartName": "top-products-revenue", "currTotal": sum(curr_series)}
        )
        return products_analytics


@analytics_rest.route("analytics/products-sold-by-net-profit")
class GetProductsSoldByetProfit(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(chart_model)
    def get(self):
        ctx = decimal.getcontext()
        ctx.rounding = decimal.ROUND_HALF_UP
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]

        products = (
            SaleItem.query.filter(SaleItem.date_created <= date_end)
            .filter(SaleItem.date_created >= date_start)
            .with_entities(
                SaleItem.id.label("id"),
                SaleItem.date_created.label("date_created"),
                SaleItem.product_name.label("product_name"),
                sa.func.sum(SaleItem.net_profit_amount).label("net_profit_amount"),
            )
            .group_by(SaleItem.product_name)
            .order_by(sa.func.sum(SaleItem.net_profit_amount).desc())
            .limit(10)
            .all()
        )

        products_analytics = {"options": [], "series": [], "info": {}}
        curr_series = []

        for item in products:
            products_analytics["options"].append(item.product_name)
            curr_series.append(Decimal(item.net_profit_amount).quantize(TWOPLACES))

        products_analytics["series"].append({"name": "revenue", "data": curr_series})
        products_analytics["info"].update(
            {"chartName": "top-products-revenue", "currTotal": sum(curr_series)}
        )
        return products_analytics


@analytics_rest.route("analytics/products/<int:id>")
class GetProductStats(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(percentage_model)
    def get(self, id):
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]
        prev_date_start = request_dates["prev_date_start"]
        prev_date_end = request_dates["prev_date_end"]

        curr_products = SaleItem.query.filter(SaleItem.date_created <= date_end).filter(
            SaleItem.date_created >= date_start
        )

        prev_products = SaleItem.query.filter(
            SaleItem.date_created <= prev_date_end
        ).filter(SaleItem.date_created >= prev_date_start)

        if id:
            curr_products = curr_products.filter_by(product_id=id)
            prev_products = prev_products.filter_by(product_id=id)
        else:
            raise NotFound("Product with this id does not exist!")

        curr_products = (
            curr_products.with_entities(
                SaleItem.id.label("id"),
                SaleItem.date_created.label("date_created"),
                sa.func.sum(SaleItem.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", SaleItem.date_created))
            .order_by(SaleItem.date_created)
            .all()
        )

        prev_products = (
            prev_products.with_entities(
                SaleItem.id.label("id"),
                SaleItem.date_created.label("date_created"),
                sa.func.sum(SaleItem.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", SaleItem.date_created))
            .order_by(SaleItem.date_created)
            .all()
        )

        products_analytics = {"options": [], "series": [], "info": {}}

        dates = get_curr_prev_chart(date_start, date_end, curr_products, prev_products)

        curr_comp_series = dates["curr_series"]
        prev_comp_series = dates["prev_series"]
        products_analytics["options"] = dates["options"]
        curr_total = sum(curr_comp_series)
        prev_total = sum(prev_comp_series)

        products_analytics["series"].append(
            {"name": "revenue", "data": curr_comp_series}
        )
        products_analytics["series"].append(
            {"name": "revenuePreviousPeriod", "data": prev_comp_series}
        )

        percentage_diff = get_percentage_change(
            Decimal(curr_total), Decimal(prev_total)
        )
        products_analytics["info"].update(
            {
                "chartName": "product-stats",
                "currTotal": curr_total,
                "prevTotal": prev_total,
                "percentageDiff": percentage_diff,
            }
        )
        return products_analytics


@analytics_rest.route("analytics/users-revenue")
class GetTopUsers(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(chart_model)
    def get(self):
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]

        users = (
            Sale.query.filter(Sale.date_created <= date_end)
            .filter(Sale.date_created >= date_start)
            .with_entities(
                Sale.id.label("id"),
                Sale.date_created.label("date_created"),
                Sale.user_id.label("user_id"),
                sa.func.sum(Sale.total_amount).label("total_amount"),
            )
            .group_by(Sale.user_id)
            .order_by(sa.func.sum(Sale.total_amount))
            .limit(10)
            .all()
        )

        users_analytics = {"options": [], "series": [], "info": {}}
        curr_series = []

        for item in users:
            user = User.query.filter_by(id=item.user_id).first()
            users_analytics["options"].append(user.first_name + " " + user.last_name)
            curr_series.append(item.total_amount)

        users_analytics["series"].append({"name": "revenue", "data": curr_series})
        users_analytics["info"].update(
            {"chartName": "top-users-revenue", "currTotal": sum(curr_series)}
        )
        return users_analytics


@analytics_rest.route("analytics/users/<int:id>")
class GetUserStats(Resource):
    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    @analytics_rest.marshal_with(percentage_model)
    def get(self, id):
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        date_start = request_dates["date_start"]
        date_end = request_dates["date_end"]
        prev_date_start = request_dates["prev_date_start"]
        prev_date_end = request_dates["prev_date_end"]

        curr_user_analytics = Sale.query.filter(Sale.date_created <= date_end).filter(
            Sale.date_created >= date_start
        )

        prev_user_analytics = Sale.query.filter(
            Sale.date_created <= prev_date_end
        ).filter(Sale.date_created >= prev_date_start)

        if id:
            curr_user_analytics = curr_user_analytics.filter_by(user_id=id)
            prev_user_analytics = prev_user_analytics.filter_by(user_id=id)
        else:
            logged_in_user = currentUser(request)
            curr_user_analytics = curr_user_analytics.filter_by(
                user_id=logged_in_user.id
            )
            prev_user_analytics = prev_user_analytics.filter_by(
                user_id=logged_in_user.id
            )

        curr_user_analytics = (
            curr_user_analytics.with_entities(
                Sale.id.label("id"),
                Sale.date_created.label("date_created"),
                sa.func.sum(Sale.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))
            .order_by(Sale.date_created)
            .all()
        )

        prev_user_analytics = (
            prev_user_analytics.with_entities(
                Sale.id.label("id"),
                Sale.date_created.label("date_created"),
                sa.func.sum(Sale.total_amount).label("total_amount"),
            )
            .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))
            .order_by(Sale.date_created)
            .all()
        )

        user_analytics = {"options": [], "series": [], "info": {}}

        dates = get_curr_prev_chart(
            date_start, date_end, curr_user_analytics, prev_user_analytics
        )

        curr_comp_series = dates["curr_series"]
        prev_comp_series = dates["prev_series"]
        user_analytics["options"] = dates["options"]
        curr_total = sum(curr_comp_series)
        prev_total = sum(prev_comp_series)

        user_analytics["series"].append({"name": "revenue", "data": curr_comp_series})
        user_analytics["series"].append(
            {"name": "revenuePreviousPeriod", "data": prev_comp_series}
        )

        percentage_diff = get_percentage_change(
            Decimal(curr_total), Decimal(prev_total)
        )
        user_analytics["info"].update(
            {
                "chartName": "product-stats",
                "currTotal": curr_total,
                "prevTotal": prev_total,
                "percentageDiff": percentage_diff,
            }
        )
        return user_analytics


@analytics_rest.route("analytics/products/all")
class ProductsAnalyticsAll(Resource):
    date_start = None
    date_end = None

    @analytics_rest.doc(params={"start_date": "", "end_date": ""})
    def get(self):
        args = parser.parse_args()
        start_date = args["start_date"]
        end_date = args["end_date"]
        request_dates = get_curr_prev_dates(start_date, end_date)
        self.date_start = request_dates["date_start"]
        self.date_end = request_dates["date_end"]
        data = self.main()
        return data

    def format_data_for_chart(self, json_data):
        categories = [item["product_name"] for item in json_data]
        quantity_sold = [item["quantity_sold"] for item in json_data]
        total_amount = [item["total_amount"] for item in json_data]
        gross_profit_amount = [item["gross_profit_amount"] for item in json_data]

        formatted_data = {
            "categories": categories,
            "series": [
                {"name": "quantity", "data": quantity_sold},
                {"name": "total_amount", "data": total_amount},
                {"name": "gross_profit_amount", "data": gross_profit_amount},
            ],
            "total_products": len(json_data),
        }

        return formatted_data

    def extract_data(self):
        query = (
            db.session.query(
                SaleItem.product_id,
                SaleItem.product_name,
                SaleItem.date_created.label("date_sold"),
                db.func.sum(SaleItem.product_quantity).label("quantity_sold"),
                db.func.sum(Sale.total_amount).label("total_amount"),
                db.func.sum(Sale.gross_profit_amount).label("gross_profit_amount"),
            )
            .join(Sale, Sale.id == SaleItem.sale_id)  # Join with the Sale table
            .filter(SaleItem.date_created >= self.date_start)  # Filter for start date
            .filter(SaleItem.date_created <= self.date_end)  # Filter for end date
            .group_by(SaleItem.product_id)
            .order_by(SaleItem.date_created)
            .all()
        )

        # Convert query result to a DataFrame
        df = pd.DataFrame(
            query,
            columns=[
                "product_id",
                "product_name",
                "date_sold",
                "quantity_sold",
                "total_amount",
                "gross_profit_amount",
            ],
        )

        return df

    def process_data(self, df):
        # Convert Decimal to float for necessary columns
        df["quantity_sold"] = df["quantity_sold"].astype(float)
        df["total_amount"] = df["total_amount"].astype(float)
        df["gross_profit_amount"] = df["gross_profit_amount"].astype(float)

        # Calculate ranks for each criterion
        df["rank_quantity"] = df["quantity_sold"].rank(ascending=False)
        df["rank_total_amount"] = df["total_amount"].rank(ascending=False)
        df["rank_gross_profit"] = df["gross_profit_amount"].rank(ascending=False)

        # Calculate combined rank (simple average of the three ranks)
        df["combined_rank"] = df[
            ["rank_quantity", "rank_total_amount", "rank_gross_profit"]
        ].mean(axis=1)

        return df

    def main(self):
        df = self.extract_data()

        processed_df = self.process_data(df)
        df_sorted = processed_df.sort_values(by="combined_rank", ascending=True)
        data = df_sorted.head(10).to_dict(orient="records")
        return jsonify(self.format_data_for_chart(data))
