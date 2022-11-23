from datetime import datetime, date, time
from flask import Blueprint, request, jsonify, request
from website.models.settings import Settings
from website.models.product import Product
from website.models.sale import Sale, SaleItem, SaleTax
from website.models.user import User
from website.helpers import getPaginatedDict, sumListOfDicts
from website.jsonify.settings import getTaxesList
from website.jsonify.sale import getSalesList, getSaleItemsList, getDailySalesList, getSaleDict
from website import db
from sqlalchemy import or_, asc, desc, func
import sqlalchemy as sa
from decimal import *
from website.token import currentUser

sale = Blueprint('sale', __name__)

@sale.route('/sales', methods=["POST"])
def createSale():
    products = request.json["products"]
    total_amount = request.json["totalAmount"]
    customer_amount = request.json["customerAmount"]
    change_amount = request.json["changeAmount"]
    current_user = currentUser(request)

    current_time = datetime.now()

    sale = Sale(
        total_amount=total_amount,
        customer_amount=customer_amount,
        change_amount=change_amount,
        user=current_user,
        date_created=current_time,
        date_modified=current_time,
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
            date_created=current_time,
            date_modified=current_time,
        )
        stock_diff = product_query.stock - Decimal(product["quantity"])
        if stock_diff >= 0:
            product_query.stock -= Decimal(product["quantity"])
        else:
            product_query.stock = 0
        
        db.session.add(sale_item)

    subtotal, sale_taxes = [], []
    taxes = Settings.query.filter_by(settings_type="tax").all()

    for item in getSaleItemsList(sale.sale_items):
        subtotal.append(item['priceWithoutTax'] * Decimal(item['quantity']))
        for tax in taxes:
            if item['product']['tax'] == int(tax.settings_value):
                key_v = tax.settings_name + "+" + tax.settings_alias
                sale_taxes.append({key_v: item['taxAmount'] * Decimal(item['quantity'])})
    
    sale.subtotal_amount = sum(subtotal)
    sale_taxes = sumListOfDicts(sale_taxes)
    for key, value in sale_taxes.items():
        split_key = key.split("+")
        db.session.add(
            SaleTax(
                sale=sale, 
                tax_name=str(split_key[0]), 
                tax_alias=str(split_key[1]), 
                tax_value=value,
                date_created=current_time,
                date_modified=current_time,
            )
        )
    db.session.commit()
    
    return jsonify("success"), 200

@sale.route('/sales', methods=["GET"])
def getSales():
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)

    sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)
    
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

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
        
    paginated_items = Sale.query.filter(or_(
        Sale.id.ilike(looking_for),
        Sale.total_amount.ilike(looking_for),
        Sale.subtotal_amount.ilike(looking_for),
        ))\
        .filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created > date_start)\
        .order_by(sort)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            Sale.date_modified.label("date_modified"),
            sa.func.sum(Sale.subtotal_amount).label("subtotal_amount"),
            sa.func.sum(Sale.total_amount).label("total_amount"),
            sa.func.sum(Sale.change_amount).label("change_amount"),
            sa.func.sum(Sale.customer_amount).label("customer_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .paginate(page=page, per_page=per_page)

    json_sale_items = getSalesList(paginated_items.items)

    for item in json_sale_items:
        date_split = item["dateCreated"].split(".")
        item_date = date(year=int(date_split[2][:4]), month=int(date_split[1]), day=int(date_split[0]))

        taxes = SaleTax.query.filter(SaleTax.date_created <= datetime.combine(item_date, time.max))\
            .filter(SaleTax.date_created > datetime.combine(item_date, time.min))\
            .order_by(SaleTax.tax_name.desc())\
            .with_entities(
            SaleTax.id.label("id"), 
            SaleTax.tax_name.label("tax_name"), 
            SaleTax.tax_alias.label("tax_alias"),
            sa.func.sum(SaleTax.tax_value).label("tax_value"),
        )\
        .group_by(SaleTax.tax_name).all()
        
        item["taxes"] = getTaxesList(taxes)

    return jsonify(getPaginatedDict(json_sale_items, paginated_items))

@sale.route('/sales/daily', methods=["GET"])
def getDailySales():
    sale_date = request.args.get('date', type=str)
    sale_date = sale_date.split(".")
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)

    if sort_column == "user":
        sort_column = func.lower(User.first_name)
    elif sort_column == "tax":
        sort_column = func.lower(SaleTax.tax_value)

    sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

    sale_date_start = datetime.combine(date(year=int(sale_date[2]), month=int(sale_date[1]), day=int(sale_date[0])), time.min)
    sale_date_end = datetime.combine(date(year=int(sale_date[2]), month=int(sale_date[1]), day=int(sale_date[0])), time.max)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
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
        ))\
        .order_by(sort)\
        .filter(Sale.date_created <= sale_date_end)\
        .filter(Sale.date_created >= sale_date_start)\
        .paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getDailySalesList(paginated_items.items), paginated_items))

@sale.route('/sales/<int:saleId>', methods=["GET"])
def getSaleDetails(saleId):
    sales = getSaleDict(Sale.query.filter_by(id=saleId).first_or_404())
    sale_items = getSaleItemsList(SaleItem.query.filter_by(sale_id=saleId).all())
    sale_taxes = getTaxesList(SaleTax.query.filter_by(sale_id=saleId).all())
    sales["saleItems"] = sale_items
    sales["taxes"] = sale_taxes
    return jsonify(sales)