from flask import Blueprint, request, jsonify, request
from website.models import Purchase, PurchaseItem, Product, Settings, PurchaseTax
from website.helpers import getPaginatedDict, sumListOfDicts
from website.json import getPurchasesList, getPurchaseItemsList, getSellersList
from website import db
from sqlalchemy import or_
from decimal import *
from datetime import datetime, date, time
import xlsxwriter
from pathlib import Path
import requests
from website.token import currentUser

purchase = Blueprint('purchase', __name__)
BASE_URL = "http://localhost:5000"

@purchase.route('/purchases', methods=["POST"])
def createPurchase():
    products = request.json["products"]
    seller = request.json["seller"]
    total_amount = request.json["totalAmount"]
    current_user = currentUser(request)

    purchase = Purchase(
        total_amount=total_amount,
        seller_name=seller["sellerName"].lower(),
        seller_invoice_number=seller["invoiceNumber"],
        seller_fiscal_number=seller["fiscalNumber"],
        seller_tax_number=seller["taxNumber"],
        user=current_user,
        date_created=datetime.now(),
        date_modified=datetime.now(),
    )

    db.session.add(purchase)

    for product in products:
        decimal_price = Decimal(product["purchasedPrice"])
        decimal_tax = Decimal(product["tax"])
        price_without_tax = decimal_price - (decimal_tax / 100) * decimal_price
        tax_amount = (decimal_tax / 100) * decimal_price

        product_query = Product.query.filter_by(barcode=product["barcode"]).first()
				
        if product_query:
            purchase_item = PurchaseItem(
                purchase=purchase,
                product_id=product_query.id,
                product_barcode=product_query.barcode,
                product_name=product["productName"],
                product_tax=product["tax"],
                product_purchased_price=product["purchasedPrice"],
                product_selling_price=product["sellingPrice"],
                product_stock=Decimal(product["stock"]),
                price_without_tax=price_without_tax,
                tax_amount=tax_amount,
                total_amount=Decimal(Decimal(product["purchasedPrice"]) * Decimal(product["stock"])),
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )

            product_query.name = product["productName"].lower()
            product_query.tax = product["tax"]
            product_query.purchased_price = product["purchasedPrice"]
            product_query.selling_price = product["sellingPrice"]
            product_query.stock += Decimal(product["stock"])
        else:
            created_product = Product(
                name=product["productName"].lower(), 
                barcode=product["barcode"], 
                stock=product["stock"], 
                tax=product["tax"], 
                purchased_price=product["purchasedPrice"], 
                selling_price= product["sellingPrice"],
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )

            db.session.add(created_product)
            db.session.commit()

            purchase_item = PurchaseItem(
                purchase=purchase,
                product_id=created_product.id,
                product_barcode=created_product.barcode,
                product_name=created_product.name,
                product_tax=created_product.tax,
                product_purchased_price=created_product.purchased_price,
                product_selling_price=created_product.selling_price,
                product_stock=created_product.stock,
                price_without_tax=price_without_tax,
                tax_amount=tax_amount,
                total_amount=Decimal(created_product.purchased_price * Decimal(created_product.stock)),
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )
        db.session.add(purchase_item)

    subtotal, purchase_taxes = [], []
    taxes = Settings.query.filter_by(settings_type="tax").all()

    for item in getPurchaseItemsList(purchase.purchase_items):
        subtotal.append(item['priceWithoutTax'] * Decimal(item['product']['stock']))
        for tax in taxes:
            if item['product']['tax'] == int(tax.settings_value):
                key_v = tax.settings_name + "+" + tax.settings_alias
                purchase_taxes.append({key_v: item['taxAmount'] * Decimal(item['product']['stock'])})
    
    purchase.subtotal_amount = sum(subtotal)
    purchase_taxes = sumListOfDicts(purchase_taxes)
    for key, value in purchase_taxes.items():
        split_key = key.split("+")
        db.session.add(
            PurchaseTax(
                purchase=purchase, 
                tax_name=str(split_key[0]), 
                tax_alias=str(split_key[1]), 
                tax_value=value
            )
        )
    db.session.commit()
    
    return jsonify("Success"), 200

@purchase.route('/purchases', methods=["GET"])
def getPurchases():
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
        
    paginated_items = Purchase.query.filter(or_(
        Purchase.id.ilike(looking_for),
        Purchase.seller_name.ilike(looking_for),
        Purchase.seller_invoice_number.ilike(looking_for),
        Purchase.seller_fiscal_number.ilike(looking_for),
        Purchase.seller_tax_number.ilike(looking_for),
        ))\
        .filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created > date_start)

    if (desc):
        paginated_items = paginated_items.order_by(Purchase.id.desc())

    paginated_items = paginated_items.paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getPurchasesList(paginated_items.items), paginated_items))

@purchase.route('/sellers', methods=["GET"])
def getSellers():
    desc = request.args.get('desc', True, type=bool)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '*', type=str)

    if '*' in search or '_' in search: 
        looking_for = search.replace('_', '__')\
            .replace('*', '%')\
            .replace('?', '_')
    else:
        looking_for = '%{0}%'.format(search)
        
    paginated_items = Purchase.query.filter(or_(
        Purchase.id.ilike(looking_for),
        Purchase.seller_name.ilike(looking_for),
        Purchase.seller_invoice_number.ilike(looking_for),
        Purchase.seller_fiscal_number.ilike(looking_for),
        Purchase.seller_tax_number.ilike(looking_for),
        ))\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.seller_name.label("seller_name"), 
            Purchase.seller_fiscal_number.label("seller_fiscal_number"), 
            Purchase.seller_tax_number.label("seller_tax_number"), 
            Purchase.seller_invoice_number.label("seller_invoice_number"), 
            Purchase.date_created.label("date_created"), 
            Purchase.date_modified.label("date_modified"), 
        )\
        .group_by(Purchase.seller_name)\

    if (desc):
        paginated_items = paginated_items.order_by(Purchase.id.desc())

    paginated_items = paginated_items.paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getSellersList(paginated_items.items), paginated_items))

@purchase.route('/purchases/<int:purchaseId>', methods=["GET"])
def getPurchaseDetails(purchaseId):
    purchases = Purchase.query.filter_by(id=purchaseId).all()
    return jsonify(getPurchasesList(purchases)[0])

@purchase.route('/sellers/<string:name>', methods=["GET"])
def getSellerDetails(name):
    purchase = Purchase.query.filter_by(seller_name=name).first_or_404()
    return jsonify(getSellerDetails([purchase, purchase])[0])

@purchase.route('/purchases/download-exel', methods=["GET"])
def downloadPurchasesExcel():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    file_name = request.args.get('fileName', 'excelFile', type=str)

    api_response = requests.get(f'{BASE_URL}/api/purchases?page={page}&per_page={per_page}&startDate={custom_start_date}&endDate={custom_end_date}&desc=')
    purchases = api_response.json()["data"]

    FILENAME = file_name.upper() + ".xlsx"
    downloads_path = str(Path.home() / "Downloads" / FILENAME)
    workbook = xlsxwriter.Workbook(downloads_path)
 
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 9, 20)
    
    header_format = workbook.add_format({'bold': True, 'bg_color': 'gray', 'align': 'center'})

    euro = workbook.add_format({'num_format': '€#,##0.00'})

    worksheet.write('A1', 'Date', header_format)
    worksheet.write('B1', 'Seller Name', header_format)
    worksheet.write('C1', 'Invoice Number', header_format)
    worksheet.write('D1', 'Fiscal Number', header_format)
    worksheet.write('E1', 'Tax Number', header_format)
    worksheet.write('F1', '8%', header_format)
    worksheet.write('G1', '18%', header_format)
    worksheet.write('H1', 'Subtotal', header_format)
    worksheet.write('I1', 'Total', header_format)

    row = 1
    col = 0

    for item in purchases:
        worksheet.write(row, col, item["dateCreated"][0:10])
        worksheet.write(row, col + 1, item["sellerName"])
        worksheet.write(row, col + 2, item["sellerInvoiceNumber"])
        worksheet.write(row, col + 3, item["sellerFiscalNumber"])
        worksheet.write(row, col + 4, item["sellerTaxNumber"])
        worksheet.write(row, col + 5, item["eightTaxAmount"], euro)
        worksheet.write(row, col + 6, item["eighteenTaxAmount"], euro)
        worksheet.write(row, col + 7, item["subTotalAmount"], euro)
        worksheet.write(row, col + 8, item["totalAmount"], euro)

        row += 1
        
    workbook.close()

    return jsonify(downloads_path)