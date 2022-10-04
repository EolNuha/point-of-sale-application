from datetime import datetime, date, timedelta, time
from flask import Blueprint, request, jsonify, request
from website.models import Sale, SaleItem, Product
from website.helpers import getPaginatedDict, getSalesList, getSaleItemsList
from website import db
from sqlalchemy import or_
import sqlalchemy as sa
from decimal import *
import xlsxwriter
from pathlib import Path
import calendar
import time as tm

sale = Blueprint('sale', __name__)


MONTHS = {
    "January": 1,
    "Febuarary": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}

@sale.route('/sales', methods=["POST"])
def createSale():
    products = request.json["products"]
    total_amount = request.json["totalAmount"]
    customer_amount = request.json["customerAmount"]
    change_amount = request.json["changeAmount"]

    sale = Sale(
        total_amount=total_amount,
        customer_amount=customer_amount,
        change_amount=change_amount,
    )

    db.session.add(sale)
    

    for product in products:
        decimal_price = Decimal(product["sellingPrice"])
        decimal_tax = Decimal(product["tax"])
        price_without_tax = decimal_price - (decimal_tax / 100) * decimal_price
        tax_amount = (decimal_tax / 100) * decimal_price

        product_query = Product.query.filter_by(id=product["id"]).one()
        sale_item = SaleItem(
            sale=sale,
            product_id=product_query.id,
            product_barcode=product_query.barcode,
            product_name=product_query.name,
            product_tax=product_query.tax,
            product_purchased_price=product_query.purchased_price,
            product_selling_price=product_query.selling_price,
            product_quantity=Decimal(product["quantity"]),
            price_without_tax=price_without_tax,
            tax_amount=tax_amount
        )

        product_query.stock -= Decimal(product["quantity"])
        
        db.session.add(sale_item)

    subtotal, eight, eighteen = [], [], []

    for item in getSaleItemsList(sale.sale_items):
        subtotal.append(item['priceWithoutTax'] * Decimal(item['quantity']))
        if item['product']['tax'] == 8:
            eight.append(item['taxAmount'] * Decimal(item['quantity']))
        if item['product']['tax'] == 18:
            eighteen.append(item['taxAmount'] * Decimal(item['quantity']))
    
    sale.subtotal_amount = sum(subtotal)
    sale.eight_tax_amount = sum(eight)
    sale.eighteen_tax_amount = sum(eighteen)
    
    db.session.commit()
    
    return jsonify("success"), 200

@sale.route('/sales', methods=["GET"])
def getSales():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)

    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")
    # month = request.args.get('month', "October", type=str)
    # year = request.args.get('year', 2022, type=int)
    # month = request.args.get('month', "October", type=str)
    # cal = calendar.monthrange(year, MONTHS[month])
    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end =  datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '*', type=str)

    if '*' in search or '_' in search: 
        looking_for = search.replace('_', '__')\
            .replace('*', '%')\
            .replace('?', '_')
    else:
        looking_for = '%{0}%'.format(search)
        
    paginated_items = Sale.query.filter(or_(
        Sale.id.ilike(looking_for),
        ))\
        .filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created > date_start)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            Sale.date_modified.label("date_modified"),
            sa.func.sum(Sale.subtotal_amount).label("subtotal_amount"),
            sa.func.sum(Sale.total_amount).label("total_amount"),
            sa.func.sum(Sale.change_amount).label("change_amount"),
            sa.func.sum(Sale.customer_amount).label("customer_amount"),
            sa.func.sum(Sale.eight_tax_amount).label("eight_tax_amount"),
            sa.func.sum(Sale.eighteen_tax_amount).label("eighteen_tax_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .paginate(page=page, per_page=per_page)


    return jsonify(getPaginatedDict(getSalesList(paginated_items.items), paginated_items))

@sale.route('/sales/<int:saleId>', methods=["GET"])
def getSaleDetails(saleId):
    sales = Sale.query.filter_by(id=saleId).all()
    return jsonify(getSalesList(sales)[0])

@sale.route('/sales/download-exel', methods=["POST"])
def downloadDailyExcel():
    sales = request.json["sales"]
    month = request.json["month"]
    FILENAME = month.lower() + ".xlsx"
    downloads_path = str(Path.home() / "Downloads" / FILENAME)
    workbook = xlsxwriter.Workbook(downloads_path)
 
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 6, 20)
    
    header_format = workbook.add_format({'bold': True, 'bg_color': 'gray', 'align': 'center'})

    money = workbook.add_format({'num_format': '€#,##0.00'})

    worksheet.write('A1', 'Date', header_format)
    worksheet.write('B1', 'Buyer', header_format)
    worksheet.write('C1', '8%', header_format)
    worksheet.write('D1', '18%', header_format)
    worksheet.write('E1', 'Subtotal', header_format)
    worksheet.write('F1', 'Total', header_format)

    row = 1
    col = 0

    for item in sales:
        worksheet.write(row, col, item["dateCreated"][0:10])
        worksheet.write(row, col + 1, "Qytetar")
        worksheet.write(row, col + 2, item["eightTaxAmount"], money)
        worksheet.write(row, col + 3, item["eighteenTaxAmount"], money)
        worksheet.write(row, col + 4, item["subTotalAmount"], money)
        worksheet.write(row, col + 5, item["totalAmount"], money)

        row += 1
        
    workbook.close()

    return jsonify(downloads_path)