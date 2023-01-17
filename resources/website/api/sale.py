from datetime import datetime, date, time
from flask import Blueprint, request, jsonify, request
from website.models.settings import Settings
from website.models.product import Product
from website.models.sale import Sale, SaleItem, SaleTax
from website.models.user import User
from website.helpers import getPaginatedDict, sumListOfDicts
from website.jsonify.settings import getTaxesList
from website.jsonify.sale import getSalesList, getDailySalesList, getDailySaleDict
from website import db
from sqlalchemy import or_, and_, asc, desc, func
import sqlalchemy as sa
import decimal
from website.token import currentUser
from functools import reduce

sale = Blueprint('sale', __name__)
Decimal = decimal.Decimal
FOURPLACES = Decimal(10) ** -4

@sale.route('/sales', methods=["POST"])
def createSale():
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP

    products = request.json["products"]
    total_amount = request.json["totalAmount"]
    customer_amount = request.json["customerAmount"]
    change_amount = request.json["changeAmount"]
    is_regular = request.json["isRegular"]
    current_user = currentUser(request)

    current_time = datetime.now()

    sale = Sale(
        total_amount=total_amount,
        customer_amount=customer_amount,
        change_amount=change_amount,
        user=current_user,
        is_regular=is_regular,
        date_created=current_time,
        date_modified=current_time,
    )

    db.session.add(sale)

    for product in products:
        product_quantity = Decimal(product["quantity"]).quantize(FOURPLACES)
        decimal_price = Decimal(product["sellingPrice"]).quantize(FOURPLACES)
        decimal_tax = Decimal(product["tax"]).quantize(FOURPLACES)
        
        tax_amount = Decimal(Decimal(decimal_tax / 100).quantize(FOURPLACES) * decimal_price).quantize(FOURPLACES)
        price_without_tax = decimal_price - tax_amount

        product_query = Product.query.filter_by(id=product["id"]).one()
        sale_item = SaleItem(
            sale=sale,
            product_id=product_query.id,
            product_barcode=product_query.barcode,
            product_name=product_query.name,
            product_tax=product_query.tax,
            product_purchased_price=product_query.purchased_price,
            product_selling_price=product_query.selling_price,
            product_measure=product_query.measure,
            product_quantity=product_quantity,
            price_without_tax=price_without_tax,
            tax_amount=tax_amount,
            total_amount=Decimal(product_query.selling_price * product_quantity).quantize(FOURPLACES),
            date_created=current_time,
            date_modified=current_time,
        )
        stock_diff = product_query.stock - product_quantity
        if stock_diff >= 0:
            product_query.stock -= product_quantity
        else:
            product_query.stock = 0
        
        db.session.add(sale_item)

    subtotal, sale_taxes, grosstotal = [], [], []
    taxes = Settings.query.filter_by(settings_type="tax").all()

    for item in sale.sale_items:
        subtotal.append(Decimal(item.price_without_tax * Decimal(item.product_quantity).quantize(FOURPLACES)).quantize(FOURPLACES))
        grosstotal.append(Decimal(item.product_purchased_price * Decimal(item.product_quantity).quantize(FOURPLACES)).quantize(FOURPLACES))
        for tax in taxes:
            if item.product_tax == int(tax.settings_value):
                key_v = tax.settings_name + "+" + tax.settings_alias
                sale_taxes.append({key_v: Decimal(item.tax_amount).quantize(FOURPLACES) * Decimal(item.product_quantity).quantize(FOURPLACES)})
    
    sale.subtotal_amount = sum(subtotal)
    sale.gross_profit_amount = Decimal(total_amount) - sum(grosstotal)
    sale_taxes = sumListOfDicts(sale_taxes)
    sale.net_profit_amount = sale.gross_profit_amount - sum(sale_taxes.values())
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
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP

    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)
    type_filter = [x == 'true' for x in request.args.getlist('type_filter[]')]
    if not type_filter: type_filter = [True, False]

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
        
    paginated_items = Sale.query\
        .join(User).filter(or_(
        Sale.id.ilike(looking_for),
        Sale.total_amount.ilike(looking_for),
        Sale.subtotal_amount.ilike(looking_for),
        User.first_name.ilike(looking_for),
        User.last_name.ilike(looking_for),
        ))\
        .filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created > date_start)\
        .filter(and_(Sale.is_regular.in_(type_filter)))\
        .order_by(sort)\
        .with_entities(
            Sale.id.label("id"), 
            Sale.date_created.label("date_created"), 
            Sale.date_modified.label("date_modified"),
            Sale.is_regular.label("is_regular"),
            sa.func.sum(Sale.subtotal_amount).label("subtotal_amount"),
            sa.func.sum(Sale.total_amount).label("total_amount"),
            sa.func.sum(Sale.gross_profit_amount).label("gross_profit_amount"),
            sa.func.sum(Sale.net_profit_amount).label("net_profit_amount"),
            sa.func.sum(Sale.change_amount).label("change_amount"),
            sa.func.sum(Sale.customer_amount).label("customer_amount"),
        )\
        .group_by(sa.func.strftime("%Y-%m-%d", Sale.date_created))\
        .paginate(page=page, per_page=per_page)

    sale_items = getSalesList(paginated_items.items)

    for item in sale_items:
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

    paginated_dict = getPaginatedDict(sale_items, paginated_items)

    total = reduce(lambda x, y: x + y['totalAmount'], sale_items, 0)
    subtotal = reduce(lambda x, y: x + y['subTotalAmount'], sale_items, 0)
    gross_total = reduce(lambda x, y: x + y['grossProfitAmount'], sale_items, 0)
    net_total = reduce(lambda x, y: x + y['netProfitAmount'], sale_items, 0)

    taxes_total = []
    for settings in Settings.query.filter_by(settings_type="tax").all():
        total_tax_value = sum(Decimal(tax['taxValue']) for item in sale_items for tax in item['taxes'] if tax['taxAlias'] == settings.settings_alias)
        taxes_total.append(
            {
                "taxAlias": settings.settings_alias, 
                "taxName": settings.settings_name, 
                "taxValue": total_tax_value
            }
        )
    
    paginated_dict["pagination"]["salesTotalAmount"] = total
    paginated_dict["pagination"]["salesSubTotalAmount"] = subtotal
    paginated_dict["pagination"]["salesTotalGrossProfit"] = gross_total
    paginated_dict["pagination"]["salesTotalNetProfit"] = net_total
    paginated_dict["pagination"]["taxes"] = taxes_total
    
    return jsonify(paginated_dict)

@sale.route('/sales-detailed', methods=["GET"])
def getSalesDetailed():
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP

    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    sort_column = request.args.get('sort_column', "date_created", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)
    type_filter = [x == 'true' for x in request.args.getlist('type_filter[]')]
    if not type_filter: type_filter = [True, False]

    if sort_column == "user":
        sort_column = func.lower(User.first_name)
    elif sort_column == "tax":
        sort_column = func.lower(SaleTax.tax_value)
    elif sort_column == "date_created":
        sort_column = Sale.date_created

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
        
    paginated_items = Sale.query\
        .join(User).filter(or_(
        Sale.id.ilike(looking_for),
        Sale.total_amount.ilike(looking_for),
        Sale.subtotal_amount.ilike(looking_for),
        User.first_name.ilike(looking_for),
        User.last_name.ilike(looking_for),
        ))\
        .filter(Sale.date_created <= date_end)\
        .filter(Sale.date_created > date_start)\
        .filter(and_(Sale.is_regular.in_(type_filter)))\
        .order_by(sort)\
        .paginate(page=page, per_page=per_page)
    
    sale_items = getDailySalesList(paginated_items.items)
    paginated_dict = getPaginatedDict(getDailySalesList(paginated_items.items), paginated_items)

    total = reduce(lambda x, y: x + y['totalAmount'], sale_items, 0)
    subtotal = reduce(lambda x, y: x + y['subTotalAmount'], sale_items, 0)
    gross_total = reduce(lambda x, y: x + y['grossProfitAmount'], sale_items, 0)
    net_total = reduce(lambda x, y: x + y['netProfitAmount'], sale_items, 0)

    taxes_total = []
    for settings in Settings.query.filter_by(settings_type="tax").all():
        total_tax_value = sum(Decimal(tax['taxValue']) for item in sale_items for tax in item['taxes'] if tax['taxAlias'] == settings.settings_alias)
        taxes_total.append(
            {
                "taxAlias": settings.settings_alias, 
                "taxName": settings.settings_name, 
                "taxValue": total_tax_value
            }
        )
    
    paginated_dict["pagination"]["salesTotalAmount"] = total
    paginated_dict["pagination"]["salesSubTotalAmount"] = subtotal
    paginated_dict["pagination"]["salesTotalGrossProfit"] = gross_total
    paginated_dict["pagination"]["salesTotalNetProfit"] = net_total
    paginated_dict["pagination"]["taxes"] = taxes_total

    return jsonify(paginated_dict)


@sale.route('/sales/daily', methods=["GET"])
def getDailySales():
    sale_date = request.args.get('date', type=str)
    sale_date = sale_date.split(".")
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)
    type_filter = [x == 'true' for x in request.args.getlist('type_filter[]')]
    if not type_filter: type_filter = [True, False]

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
        
    paginated_items = Sale.query.join(User).filter(or_(
        Sale.id.ilike(looking_for),
        Sale.total_amount.ilike(looking_for),
        Sale.subtotal_amount.ilike(looking_for),
        User.first_name.ilike(looking_for),
        User.last_name.ilike(looking_for),
        ))\
        .filter(and_(Sale.is_regular.in_(type_filter)))\
        .order_by(sort)\
        .filter(Sale.date_created <= sale_date_end)\
        .filter(Sale.date_created >= sale_date_start)\
        .paginate(page=page, per_page=per_page)

    sale_items = getDailySalesList(paginated_items.items)
    paginated_dict = getPaginatedDict(getDailySalesList(paginated_items.items), paginated_items)

    total = reduce(lambda x, y: x + y['totalAmount'], sale_items, 0)
    subtotal = reduce(lambda x, y: x + y['subTotalAmount'], sale_items, 0)
    gross_total = reduce(lambda x, y: x + y['grossProfitAmount'], sale_items, 0)
    net_total = reduce(lambda x, y: x + y['netProfitAmount'], sale_items, 0)

    taxes_total = []
    for settings in Settings.query.filter_by(settings_type="tax").all():
        total_tax_value = sum(Decimal(tax['taxValue']) for item in sale_items for tax in item['taxes'] if tax['taxAlias'] == settings.settings_alias)
        taxes_total.append(
            {
                "taxAlias": settings.settings_alias, 
                "taxName": settings.settings_name, 
                "taxValue": total_tax_value
            }
        )
    
    paginated_dict["pagination"]["salesTotalAmount"] = total
    paginated_dict["pagination"]["salesSubTotalAmount"] = subtotal
    paginated_dict["pagination"]["salesTotalGrossProfit"] = gross_total
    paginated_dict["pagination"]["salesTotalNetProfit"] = net_total
    paginated_dict["pagination"]["taxes"] = taxes_total

    return jsonify(paginated_dict)

@sale.route('/sales/<int:saleId>', methods=["GET"])
def getSaleDetails(saleId):
    return jsonify(getDailySaleDict(Sale.query.filter_by(id=saleId).first_or_404()))

@sale.route('/sales/<int:saleId>', methods=["PUT"])
def editSale(saleId):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP

    deleted_items = request.json["deletedItems"]
    saleItems = request.json["saleItems"]

    sale_query = Sale.query.filter_by(id=saleId).first_or_404()
    subtotal, sale_taxes, grosstotal = [], [], []
    taxes = Settings.query.filter_by(settings_type="tax").all()

    for item in deleted_items:
        product = Product.query.filter_by(id=item["product"]["id"]).first()
        if product: product.stock += Decimal(item["quantity"]).quantize(FOURPLACES)
        SaleItem.query.filter_by(id=item["id"]).delete()
        SaleTax.query.filter_by(sale_id=saleId).filter_by(tax_name=item["product"]["tax"]).delete()
        db.session.commit()

    for item in saleItems:
        item_quantity = Decimal(item["quantity"]).quantize(FOURPLACES)

        subtotal.append(Decimal(Decimal(item['priceWithoutTax']).quantize(FOURPLACES) * item_quantity).quantize(FOURPLACES))
        grosstotal.append(Decimal(Decimal(item['product']['purchasedPrice']) * item_quantity).quantize(FOURPLACES))
        for tax in taxes:
            if item['product']['tax'] == int(tax.settings_value):
                key_v = tax.settings_name + "+" + tax.settings_alias
                sale_taxes.append({key_v: Decimal(Decimal(item['taxAmount']).quantize(FOURPLACES) * item_quantity).quantize(FOURPLACES)})
        
        sale_item = SaleItem.query.filter_by(id=item["id"]).first()
        product = Product.query.filter_by(id=item["product"]["id"]).first()

        if product: product.stock -= (item_quantity - sale_item.product_quantity)
        sale_item.product_quantity = item_quantity
        sale_item.total_amount = Decimal(product.selling_price * item_quantity).quantize(FOURPLACES)
        db.session.commit()
    
    sale_query.subtotal_amount = sum(subtotal)
    sale_taxes = sumListOfDicts(sale_taxes)

    for key, value in sale_taxes.items():
        split_key = key.split("+")
        sale_tax = SaleTax.query.filter(SaleTax.sale_id.like(saleId), SaleTax.tax_name.ilike(split_key[0])).first()
        sale_tax.tax_value = value
        sale_tax.date_modified = datetime.now()
        db.session.commit()

    total_sum = SaleItem.query.filter_by(sale_id=saleId).with_entities(func.sum(SaleItem.total_amount).label('total')).first().total
    sale_query.total_amount = total_sum
    sale_query.gross_profit_amount = Decimal(total_sum) - sum(grosstotal)
    sale_query.net_profit_amount = sale_query.gross_profit_amount - sum(sale_taxes.values())
    db.session.commit()
    return "Success", 200

@sale.route('/sales/<int:saleId>', methods=["DELETE"])
def deleteSale(saleId):
    sale_query = Sale.query.filter_by(id=saleId).first_or_404()

    for item in sale_query.sale_items:
        product = Product.query.filter_by(id=item.product_id).first()
        if product: product.stock += item.product_quantity
        SaleItem.query.filter_by(id=item.id).delete()
        db.session.commit()
    
    SaleTax.query.filter_by(sale_id=sale_query.id).delete()
    Sale.query.filter_by(id=saleId).delete()
    db.session.commit()
    return "Success", 200