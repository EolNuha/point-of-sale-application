from flask import Blueprint, request, jsonify, request
from website.models.settings import Settings
from website.models.purchase import Purchase, PurchaseItem, PurchaseTax
from website.models.product import Product
from website.helpers import getPaginatedDict, sumListOfDicts
from website.jsonify.settings import getTaxesList
from website.jsonify.purchase import getPurchasesList, getPurchaseItemsList, getDailyPurchasesList, getDailyPurchaseDict, getSellersList, getSellerDict
from website import db
from sqlalchemy import or_, asc, desc, func
from decimal import *
from datetime import datetime, date, time
from website.token import currentUser
import sqlalchemy as sa

purchase = Blueprint('purchase', __name__)

@purchase.route('/purchases', methods=["POST"])
def createPurchase():
    products = request.json["products"]
    seller = request.json["seller"]
    total_amount = request.json["totalAmount"]
    current_user = currentUser(request)

    current_time = datetime.now()

    purchase = Purchase(
        total_amount=total_amount,
        seller_name=seller["sellerName"].lower(),
        seller_invoice_number=seller["invoiceNumber"],
        seller_fiscal_number=seller["fiscalNumber"],
        seller_tax_number=seller["taxNumber"],
        user=current_user,
        date_created=current_time,
        date_modified=current_time,
    )

    db.session.add(purchase)

    for product in products:
        decimal_price = Decimal(product["purchasedPrice"])
        decimal_tax = Decimal(product["tax"])
        price_without_tax = decimal_price - (decimal_tax / 100) * decimal_price
        tax_amount = (decimal_tax / 100) * decimal_price

        expiration_date = product["expirationDate"].split("-")
        expiration_date = datetime.combine(date(year=int(expiration_date[0]), month=int(expiration_date[1]), day=int(expiration_date[2])), time.min)

        product_query = Product.query.filter_by(name=product["productName"].lower()).first()

        found_with_barcode = Product.query.filter_by(barcode=product["barcode"]).first()
        if found_with_barcode and found_with_barcode.name != product["productName"]:
            return jsonify(
                {
                    "message": "barcodeExistsDetailed", 
                    "barcode": found_with_barcode.barcode, 
                    "product": found_with_barcode.name
                }
                ), 406
				
        if product_query:
            purchase_item = PurchaseItem(
                purchase=purchase,
                product_id=product_query.id,
                product_barcode=product["barcode"],
                product_name=product["productName"],
                product_tax=product["tax"],
                product_purchased_price=product["purchasedPrice"],
                product_selling_price=product["sellingPrice"],
                product_stock=Decimal(product["stock"]),
                price_without_tax=price_without_tax,
                tax_amount=tax_amount,
                total_amount=Decimal(Decimal(product["purchasedPrice"]) * Decimal(product["stock"])),
                date_created=current_time,
                date_modified=current_time,
            )

            product_query.name = product["productName"].lower()
            product_query.barcode = product["barcode"]
            product_query.tax = product["tax"]
            product_query.purchased_price = product["purchasedPrice"]
            product_query.selling_price = product["sellingPrice"]
            product_query.stock += Decimal(product["stock"])
            product_query.expiration_date = expiration_date
        else:
            created_product = Product(
                name=product["productName"].lower(), 
                barcode=product["barcode"], 
                stock=product["stock"], 
                tax=product["tax"], 
                purchased_price=product["purchasedPrice"], 
                selling_price= product["sellingPrice"],
                expiration_date=expiration_date,
                date_created=current_time,
                date_modified=current_time,
            )

            db.session.add(created_product)

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
                total_amount=Decimal(Decimal(created_product.purchased_price) * Decimal(created_product.stock)),
                date_created=current_time,
                date_modified=current_time,
            )
        db.session.add(purchase_item)
    db.session.commit()

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
                tax_value=value,
                date_created=current_time,
                date_modified=current_time,
            )
        )
    db.session.commit()
    
    return jsonify("Success"), 200

@purchase.route('/purchases', methods=["GET"])
def getPurchases():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)

    sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end =  datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
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
        .order_by(sort)\
        .filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created > date_start)\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            Purchase.date_modified.label("date_modified"),
            sa.func.sum(Purchase.subtotal_amount).label("subtotal_amount"),
            sa.func.sum(Purchase.total_amount).label("total_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Purchase.date_created))\
        .paginate(page=page, per_page=per_page)

    join_purchase_items = getPurchasesList(paginated_items.items)

    for item in join_purchase_items:
        date_split = item["dateCreated"].split(".")
        item_date = date(year=int(date_split[2][:4]), month=int(date_split[1]), day=int(date_split[0]))

        taxes = PurchaseTax.query.filter(PurchaseTax.date_created <= datetime.combine(item_date, time.max))\
            .filter(PurchaseTax.date_created > datetime.combine(item_date, time.min))\
            .order_by(PurchaseTax.tax_name.desc())\
            .with_entities(
            PurchaseTax.id.label("id"), 
            PurchaseTax.tax_name.label("tax_name"), 
            PurchaseTax.tax_alias.label("tax_alias"),
            sa.func.sum(PurchaseTax.tax_value).label("tax_value"),
        )\
        .group_by(PurchaseTax.tax_name).all()
        
        item["taxes"] = getTaxesList(taxes)

    return jsonify(getPaginatedDict(join_purchase_items, paginated_items))

@purchase.route('/purchases/daily', methods=["GET"])
def getDailyPurchases():
    purchase_date = request.args.get('date', type=str)
    purchase_date = purchase_date.split(".")
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)

    if sort_column == "tax":
        sort_column = func.lower(PurchaseTax.tax_value)

    sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

    purchase_date_start = datetime.combine(date(year=int(purchase_date[2]), month=int(purchase_date[1]), day=int(purchase_date[0])), time.min)
    purchase_date_end = datetime.combine(date(year=int(purchase_date[2]), month=int(purchase_date[1]), day=int(purchase_date[0])), time.max)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
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
        Purchase.total_amount.ilike(looking_for),
        Purchase.subtotal_amount.ilike(looking_for),
        ))\
        .order_by(sort)\
        .filter(Purchase.date_created <= purchase_date_end)\
        .filter(Purchase.date_created >= purchase_date_start)\
        .paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getDailyPurchasesList(paginated_items.items), paginated_items))

@purchase.route('/sellers', methods=["GET"])
def getSellers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '*', type=str)
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)

    sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

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
        .order_by(sort)\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.seller_name.label("seller_name"), 
            Purchase.seller_fiscal_number.label("seller_fiscal_number"), 
            Purchase.seller_tax_number.label("seller_tax_number"), 
            Purchase.seller_invoice_number.label("seller_invoice_number"), 
            Purchase.date_created.label("date_created"), 
            Purchase.date_modified.label("date_modified"), 
        )\
        .group_by(Purchase.seller_name).paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getSellersList(paginated_items.items), paginated_items))

@purchase.route('/purchases/<int:purchaseId>', methods=["GET"])
def getPurchaseDetails(purchaseId):
    return jsonify(getDailyPurchaseDict(Purchase.query.filter_by(id=purchaseId).first_or_404()))

@purchase.route('/sellers/<string:name>', methods=["GET"])
def getSellerDetails(name):
    purchase = Purchase.query.filter_by(seller_name=name).first_or_404()
    return jsonify(getSellerDict(purchase))