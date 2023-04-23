from flask import Blueprint, request, jsonify, request
from website.models.settings import Settings
from website.models.purchase import Purchase, PurchaseItem, PurchaseTax
from website.models.product import Product
from website.helpers import getPaginatedDict, sumListOfDicts
from website.jsonify.purchase import getTaxesList, getPurchasesList, getDailyPurchasesList, getDailyPurchaseDict, getSellersList, getSellerDict
from website import db
from sqlalchemy import or_, asc, desc, func, and_
import decimal
from datetime import datetime, date, time
from website.token import currentUser
import sqlalchemy as sa

purchase_api = Blueprint('purchase_api', __name__)
Decimal = decimal.Decimal
FOURPLACES = Decimal(10) ** -4

@purchase_api.route('/purchases', methods=["POST"])
def createPurchase():
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    current_user = currentUser(request)

    products = request.json["products"]
    seller = request.json["seller"]

    def calculate_total_price(product):
        product_purchased_price_wo_tax = Decimal(product["purchasedPrice"])
        rabat_percentage = Decimal(product["rabat"]) / 100
        tax_percentage = Decimal(product["tax"]) / 100
        stock = Decimal(product["stock"])
        price_before_tax = product_purchased_price_wo_tax - (product_purchased_price_wo_tax * rabat_percentage)
        price_after_tax = price_before_tax + (price_before_tax * tax_percentage)
        rabat_price = product_purchased_price_wo_tax * rabat_percentage * stock
        subtotal_price = price_before_tax * stock
        total_price = price_after_tax * stock
        return [total_price.quantize(FOURPLACES), subtotal_price.quantize(FOURPLACES), rabat_price.quantize(FOURPLACES)]

    total_amount = sum(calculate_total_price(product)[0] for product in products).quantize(FOURPLACES)
    subtotal_amount = sum(calculate_total_price(product)[1] for product in products).quantize(FOURPLACES)
    rabat_amount = sum(calculate_total_price(product)[2] for product in products).quantize(FOURPLACES)

    current_time = datetime.now()
    purchase_date_split = seller["purchaseDate"].split("-")
    purchase_date = datetime.combine(date(year=int(purchase_date_split[0]), month=int(purchase_date_split[1]), day=int(purchase_date_split[2])), datetime.now().time())

    purchase = Purchase(
        total_amount=total_amount,
        subtotal_amount=subtotal_amount,
        rabat_amount=rabat_amount,
        seller_name=seller["sellerName"],
        seller_invoice_number=seller["invoiceNumber"],
        seller_fiscal_number=seller["fiscalNumber"],
        seller_tax_number=seller["taxNumber"],
        purchase_type=seller["purchaseType"],
        user=current_user,
        date_created=purchase_date,
        date_modified=current_time,
    )

    db.session.add(purchase)

    for product in products:
        product_stock = Decimal(product["stock"]).quantize(FOURPLACES)
        product_purchased_price_wo_tax = Decimal(product["purchasedPrice"])
        tax_percentage = Decimal(product["tax"]) / 100
        rabat_percentage = Decimal(product["rabat"]) / 100
        price_before_tax = product_purchased_price_wo_tax - (product_purchased_price_wo_tax * rabat_percentage)
        tax_amount = Decimal(price_before_tax * tax_percentage).quantize(FOURPLACES)
        product_purchased_price = Decimal(price_before_tax + tax_amount).quantize(FOURPLACES)
        product_total_amount = Decimal(product_purchased_price * product_stock).quantize(FOURPLACES)
        if product["expirationDate"]:
            expiration_date = product["expirationDate"].split("-")
            expiration_date = datetime.combine(date(year=int(expiration_date[0]), month=int(expiration_date[1]), day=int(expiration_date[2])), time.min)
        else:
            expiration_date = None

        product_query = Product.query.filter_by(name=product["productName"]).first()
        measure = str(product["measure"])

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
                rabat=product["rabat"],
                product_purchased_price_wo_tax=product_purchased_price_wo_tax,
                product_purchased_price=product_purchased_price,
                product_selling_price=product["sellingPrice"],
                product_stock=product_stock,
                product_measure=measure,
                tax_amount=tax_amount,
                total_amount=product_total_amount,
                date_created=current_time,
                date_modified=current_time,
            )

            product_query.name = product["productName"]
            product_query.barcode = product["barcode"]
            product_query.tax = product["tax"]
            product_query.purchased_price_wo_tax = product_purchased_price_wo_tax
            product_query.purchased_price = product_purchased_price
            product_query.selling_price = product["sellingPrice"]
            product_query.measure=measure
            product_query.stock += product_stock
            product_query.expiration_date = expiration_date
        else:
            created_product = Product(
                name=product["productName"], 
                barcode=product["barcode"], 
                stock=product_stock, 
                tax=product["tax"], 
                purchased_price_wo_tax=product_purchased_price_wo_tax, 
                purchased_price=product_purchased_price, 
                selling_price= product["sellingPrice"],
                measure=measure,
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
                rabat=product["rabat"], 
                product_purchased_price_wo_tax=created_product.purchased_price_wo_tax,
                product_purchased_price=created_product.purchased_price,
                product_selling_price=created_product.selling_price,
                product_stock=created_product.stock,
                product_measure=measure,
                tax_amount=tax_amount,
                total_amount=product_total_amount,
                date_created=current_time,
                date_modified=current_time,
            )
        if(int(product["tax"]) == 0):
            tax_query = Settings(
                settings_name="0",
                settings_alias="zero",
                settings_type="tax",
                settings_value="0",
                date_created=datetime.now(),
                date_modified=datetime.now(),
            )
        else:
            tax_query = Settings.query.filter_by(settings_value=int(product["tax"])).one()
        
        tax_value = Decimal(tax_amount * product_stock).quantize(FOURPLACES)
        total_wo_tax_value = product_total_amount - tax_value
        db.session.add(
            PurchaseTax(
                purchase=purchase, 
                tax_name=tax_query.settings_name, 
                tax_alias=tax_query.settings_alias, 
                tax_value=tax_value,
                total_without_tax=total_wo_tax_value,
                date_created=current_time,
                date_modified=current_time,
            )
        )
        db.session.add(purchase_item)
    db.session.commit()
    
    return jsonify("Success"), 200

@purchase_api.route('/purchases', methods=["GET"])
def getPurchases():
    custom_start_date = request.args.get('startDate', type=str).split("-")
    custom_end_date = request.args.get('endDate', type=str).split("-")
    sort_column = request.args.get('sort_column', "date_created", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)
    type_filter = request.args.getlist('type_filter[]') or ['purchase', 'investment', 'expense']

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end =  datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '*', type=str)

    looking_for = (
        search.replace("_", "__").replace("*", "%").replace("?", "_")
        if "*" in search or "_" in search
        else f"%{search}%"
    )
        
    paginated_items = Purchase.query.filter(or_(
        Purchase.id.ilike(looking_for),
        Purchase.seller_name.ilike(looking_for),
        Purchase.seller_invoice_number.ilike(looking_for),
        Purchase.seller_fiscal_number.ilike(looking_for),
        Purchase.seller_tax_number.ilike(looking_for),
        ))\
        .order_by(asc(sort_column) if sort_dir == "asc" else desc(sort_column))\
        .filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created >= date_start)\
        .filter(and_(Purchase.purchase_type.in_(type_filter)))\
        .with_entities(
            Purchase.id.label("id"), 
            Purchase.date_created.label("date_created"), 
            Purchase.date_modified.label("date_modified"),
            sa.func.sum(Purchase.rabat_amount).label("rabat_amount"),
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
            .filter(PurchaseTax.date_created >= datetime.combine(item_date, time.min))\
            .order_by(PurchaseTax.tax_name.desc())\
            .with_entities(
            PurchaseTax.id.label("id"), 
            PurchaseTax.tax_name.label("tax_name"), 
            PurchaseTax.tax_alias.label("tax_alias"),
            sa.func.sum(PurchaseTax.tax_value).label("tax_value"),
            sa.func.sum(PurchaseTax.total_without_tax).label("total_without_tax"),
        )\
        .group_by(PurchaseTax.tax_name).all()
        
        item["taxes"] = getTaxesList(taxes)

    return jsonify(getPaginatedDict(join_purchase_items, paginated_items))

@purchase_api.route('/purchases-detailed', methods=["GET"])
def getPurchasesDetailed():
    custom_start_date = request.args.get('startDate', type=str).split("-")
    custom_end_date = request.args.get('endDate', type=str).split("-")
    sort_column = request.args.get('sort_column', "date_created", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)
    type_filter = request.args.getlist('type_filter[]') or ['purchase', 'investment', 'expense']

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end =  datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '*', type=str)

    looking_for = (
        search.replace("_", "__").replace("*", "%").replace("?", "_")
        if "*" in search or "_" in search
        else f"%{search}%"
    )
        
    paginated_items = Purchase.query\
        .filter(or_(
        Purchase.id.ilike(looking_for),
        Purchase.seller_name.ilike(looking_for),
        Purchase.seller_invoice_number.ilike(looking_for),
        Purchase.seller_fiscal_number.ilike(looking_for),
        Purchase.seller_tax_number.ilike(looking_for),
        ))\
        .order_by(asc(sort_column) if sort_dir == "asc" else desc(sort_column))\
        .filter(Purchase.date_created <= date_end)\
        .filter(Purchase.date_created >= date_start)\
        .filter(and_(Purchase.purchase_type.in_(type_filter)))\
        .paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getDailyPurchasesList(paginated_items.items), paginated_items))

@purchase_api.route('/purchases/daily', methods=["GET"])
def getDailyPurchases():
    purchase_date = request.args.get('date', type=str)
    purchase_date = purchase_date.split(".")
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)
    type_filter = request.args.getlist('type_filter[]')
    if not type_filter: type_filter = ['purchase', 'investment', 'expense']

    if sort_column == "tax":
        sort_column = func.lower(PurchaseTax.tax_value)

    purchase_date_start = datetime.combine(date(year=int(purchase_date[2]), month=int(purchase_date[1]), day=int(purchase_date[0])), time.min)
    purchase_date_end = datetime.combine(date(year=int(purchase_date[2]), month=int(purchase_date[1]), day=int(purchase_date[0])), time.max)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '*', type=str)

    looking_for = (
        search.replace("_", "__").replace("*", "%").replace("?", "_")
        if "*" in search or "_" in search
        else f"%{search}%"
    )
        
    paginated_items = Purchase.query.filter(or_(
        Purchase.id.ilike(looking_for),
        Purchase.seller_name.ilike(looking_for),
        Purchase.seller_invoice_number.ilike(looking_for),
        Purchase.total_amount.ilike(looking_for),
        Purchase.subtotal_amount.ilike(looking_for),
        ))\
        .order_by(asc(sort_column) if sort_dir == "asc" else desc(sort_column))\
        .filter(Purchase.date_created <= purchase_date_end)\
        .filter(Purchase.date_created >= purchase_date_start)\
        .filter(and_(Purchase.purchase_type.in_(type_filter)))\
        .paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getDailyPurchasesList(paginated_items.items), paginated_items))

@purchase_api.route('/sellers', methods=["GET"])
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

@purchase_api.route('/purchases/<int:purchaseId>', methods=["GET"])
def getPurchaseDetails(purchaseId):
    return jsonify(getDailyPurchaseDict(Purchase.query.filter_by(id=purchaseId).first_or_404()))

@purchase_api.route('/sellers/<string:name>', methods=["GET"])
def getSellerDetails(name):
    purchase = Purchase.query.filter_by(seller_name=name).first_or_404()
    return jsonify(getSellerDict(purchase))

@purchase_api.route('/purchases/<int:purchaseId>', methods=["PUT"])
def editPurchase(purchaseId):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP

    deleted_items = request.json["deletedItems"]
    purchaseItems = request.json["purchaseItems"]

    purchase_query = Purchase.query.filter_by(id=purchaseId).first_or_404()
    subtotal, purchase_taxes = [], []
    taxes = Settings.query.filter_by(settings_type="tax").all()

    for item in deleted_items:
        product = Product.query.filter_by(barcode=item["product"]["barcode"]).first()
        if product: product.stock -= Decimal(item["product"]["stock"])
        PurchaseItem.query.filter_by(id=item["id"]).delete()
        PurchaseTax.query.filter_by(purchase_id=purchaseId).filter_by(tax_name=item["product"]["tax"]).delete()
        db.session.commit()

    for item in purchaseItems:
        item_stock = Decimal(item["product"]["stock"]).quantize(FOURPLACES)
        item_purchased_price = Decimal(item["product"]["purchasedPrice"]).quantize(FOURPLACES)
        item_tax = Decimal(item["product"]["tax"]).quantize(FOURPLACES)
        tax_amount = Decimal(Decimal(item_tax / 100).quantize(FOURPLACES) * item_purchased_price).quantize(FOURPLACES)
        item_purchased_price_wo_tax = item_purchased_price - tax_amount

        subtotal.append(Decimal(item_purchased_price_wo_tax * item_stock).quantize(FOURPLACES))

        for tax in taxes:
            if item['product']['tax'] == int(tax.settings_value):
                key_v = tax.settings_name + "+" + tax.settings_alias
                purchase_taxes.append({key_v: tax_amount * item_stock})
        
        purchase_item = PurchaseItem.query.filter_by(id=item["id"]).first()

        purchase_item.product_stock = item_stock
        purchase_item.product_purchased_price_wo_tax = item_purchased_price_wo_tax
        purchase_item.product_purchased_price = item_purchased_price
        purchase_item.tax_amount = tax_amount
        purchase_item.total_amount = Decimal(Decimal(item_purchased_price).quantize(FOURPLACES) * Decimal(item_stock)).quantize(FOURPLACES)

        product = Product.query.filter_by(barcode=item["product"]["barcode"]).first()
        if product:
            product.stock += (item_stock - purchase_item.product_stock)
            product.purchased_price_wo_tax = item_purchased_price_wo_tax
            product.purchased_price = item_purchased_price
    
        db.session.commit()

    purchase_query.subtotal_amount = sum(subtotal)
    purchase_taxes = sumListOfDicts(purchase_taxes)

    for key, value in purchase_taxes.items():
        split_key = key.split("+")
        purchase_tax = PurchaseTax.query.filter(PurchaseTax.purchase_id.like(purchaseId), PurchaseTax.tax_name.ilike(split_key[0])).first()
        purchase_tax.tax_value = value
        purchase_tax.date_modified = datetime.now()
        db.session.commit()

    total_sum = PurchaseItem.query.filter_by(purchase_id=purchaseId).with_entities(func.sum(PurchaseItem.total_amount).label('total')).first().total
    purchase_query.total_amount = total_sum
    db.session.commit()
    return "Success", 200

@purchase_api.route('/purchases/<int:purchaseId>', methods=["DELETE"])
def deletePurchase(purchaseId):
    purchase_query = Purchase.query.filter_by(id=purchaseId).first_or_404()

    for item in purchase_query.purchase_items:
        product = Product.query.filter_by(id=item.product_id).first()
        if product: product.stock -= Decimal(item.product_stock)
        PurchaseItem.query.filter_by(id=item.id).delete()
        db.session.commit()
    
    PurchaseTax.query.filter_by(purchase_id=purchase_query.id).delete()
    Purchase.query.filter_by(id=purchaseId).delete()
    db.session.commit()
    return "Success", 200