from datetime import datetime, date, timedelta, time
from flask import Blueprint, request, jsonify, request
from website.models import Sale, SaleItem, Product, User
from website.helpers import getPaginatedDict, getSalesList, getSaleItemsList, getDailySalesList
from website import db
from sqlalchemy import desc, or_
import sqlalchemy as sa
from decimal import *
import xlsxwriter
from pathlib import Path
import requests
from website.token import token_required, currentUser

sale = Blueprint('sale', __name__)
BASE_URL = "http://localhost:5000"

@sale.route('/sales', methods=["POST"])
def createSale():
    products = request.json["products"]
    total_amount = request.json["totalAmount"]
    customer_amount = request.json["customerAmount"]
    change_amount = request.json["changeAmount"]
    current_user = currentUser(request)

    sale = Sale(
        total_amount=total_amount,
        customer_amount=customer_amount,
        change_amount=change_amount,
        user=current_user,
        date_created=datetime.now(),
        date_modified=datetime.now(),
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
            tax_amount=tax_amount,
            total_amount=Decimal(product_query.selling_price * Decimal(product["quantity"])),
            date_created=datetime.now(),
            date_modified=datetime.now(),
        )
        stock_diff = product_query.stock - Decimal(product["quantity"])
        if stock_diff >= 0:
            product_query.stock -= Decimal(product["quantity"])
        else:
            product_query.stock = 0
        
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
    desc = request.args.get('desc', True, type=bool)
    
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

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
        Sale.total_amount.ilike(looking_for),
        Sale.subtotal_amount.ilike(looking_for),
        Sale.eight_tax_amount.ilike(looking_for),
        Sale.eighteen_tax_amount.ilike(looking_for),
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
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))

    if (desc):
        paginated_items = paginated_items.order_by(Sale.id.desc())

    paginated_items = paginated_items.paginate(page=page, per_page=per_page)


    return jsonify(getPaginatedDict(getSalesList(paginated_items.items), paginated_items))

@sale.route('/sales/daily', methods=["GET"])
def getDailySales():
    sale_date = request.args.get('date', type=str)
    sale_date = sale_date.split(".")
    desc = request.args.get('desc', True, type=bool)

    sale_date_start = datetime.combine(date(year=int(sale_date[2]), month=int(sale_date[1]), day=int(sale_date[0])), time.min)
    sale_date_end = datetime.combine(date(year=int(sale_date[2]), month=int(sale_date[1]), day=int(sale_date[0])), time.max)
    
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
        Sale.total_amount.ilike(looking_for),
        Sale.subtotal_amount.ilike(looking_for),
        Sale.eight_tax_amount.ilike(looking_for),
        Sale.eighteen_tax_amount.ilike(looking_for),
        ))\
        .filter(Sale.date_created <= sale_date_end)\
        .filter(Sale.date_created >= sale_date_start)

    if (desc):
        paginated_items = paginated_items.order_by(Sale.id.desc())

    paginated_items = paginated_items.paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getDailySalesList(paginated_items.items), paginated_items))

@sale.route('/sales/<int:saleId>', methods=["GET"])
def getSaleDetails(saleId):
    sales = getSalesList(Sale.query.filter_by(id=saleId).all())[0]
    sale_items = getSaleItemsList(SaleItem.query.filter_by(sale_id=saleId).all())
    sales["saleItems"] = sale_items
    return jsonify(sales)

@sale.route('/sales/download-exel', methods=["GET"])
def downloadSalesExcel():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    file_name = request.args.get('fileName', 'excelFile', type=str)
    daily = request.args.get('dailySales', False, type=bool)
    daily_date = request.args.get('dailyDate', type=str)
    
    if daily:
        URL = f'{BASE_URL}/api/sales/daily?page={page}&per_page={per_page}&date={daily_date}&desc='
    else:
        URL = f'{BASE_URL}/api/sales?page={page}&per_page={per_page}&startDate={custom_start_date}&endDate={custom_end_date}&desc='

    api_response = requests.get(URL)
    sales = list(api_response.json()["data"])

    FILENAME = file_name.upper() + ".xlsx"
    downloads_path = str(Path.home() / "Downloads" / FILENAME)
    workbook = xlsxwriter.Workbook(downloads_path)
 
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 6, 20)
    
    header_format = workbook.add_format({'bold': True, 'bg_color': 'gray', 'align': 'center'})

    euro = workbook.add_format({'num_format': '€#,##0.00'})

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
        worksheet.write(row, col + 2, Decimal(item["eightTaxAmount"]), euro)
        worksheet.write(row, col + 3, Decimal(item["eighteenTaxAmount"]), euro)
        worksheet.write(row, col + 4, Decimal(item["subTotalAmount"]), euro)
        worksheet.write(row, col + 5, Decimal(item["totalAmount"]), euro)

        row += 1
        
    workbook.close()

    return jsonify(downloads_path)

@sale.route('/sales/demo', methods=["GET"])
def createDemoSales():
    current_user = User.query.first()
    demo = [
        [100, 100, 0, "2022-10-1"],
        [95, 100, 5, "2022-10-2"],
        [80, 100, 20, "2022-10-3"],
        [55, 60, 5, "2022-10-4"],
        [43.2, 45, 1.8, "2022-10-5"],
        [30, 10, 0, "2022-10-6"],
        [55, 20, 5, "2022-10-7"],
        [40, 5, 1, "2022-10-8"],
        [100, 100, 0, "2022-10-9"],
        [93.2, 95, 0, "2022-10-10"],
        [85.25, 90, 0, "2022-10-11"],
        [150, 150, 0, "2022-10-12"],
        [100, 100, 0, "2022-10-13"],
    ]
    for index, i in enumerate(demo):
        sale_date = i[3].split("-")
        s = Sale(
            total_amount=i[0],
            customer_amount=i[1],
            change_amount=i[2],
            eight_tax_amount=5,
            eighteen_tax_amount=10,
            subtotal_amount=5,
            user=current_user,
            date_created=datetime.combine(date(year=int(sale_date[0]), month=int(sale_date[1]), day=int(sale_date[2])), time.min),
            date_modified=datetime.combine(date(year=int(sale_date[0]), month=int(sale_date[1]), day=int(sale_date[2])), time.min)
        )
        db.session.add(s)
        db.session.commit()

        products = Product.query.limit(10).all()
        for productIdx, product in enumerate(products):
            decimal_price = Decimal(product.selling_price)
            decimal_tax = Decimal(product.tax)
            price_without_tax = decimal_price - (decimal_tax / 100) * decimal_price
            tax_amount = (decimal_tax / 100) * decimal_price
            sale_item = SaleItem(
                sale=s,
                product_id=product.id,
                product_barcode=product.barcode,
                product_name=product.name,
                product_tax=product.tax,
                product_purchased_price=product.purchased_price,
                product_selling_price=product.selling_price,
                product_quantity=Decimal(productIdx + 1),
                price_without_tax=price_without_tax,
                tax_amount=tax_amount,
                total_amount=Decimal(product.selling_price * (productIdx + 1)),
                date_created=datetime.combine(date(year=int(sale_date[0]), month=int(sale_date[1]), day=int(sale_date[2])), time.min),
                date_modified=datetime.combine(date(year=int(sale_date[0]), month=int(sale_date[1]), day=int(sale_date[2])), time.min)
            )
            
            db.session.add(sale_item)
            db.session.commit()
    return "success", 200