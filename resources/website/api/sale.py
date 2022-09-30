from flask import Blueprint, request, jsonify, request
from website.models import Sale, SaleItem, Product
from website.helpers import getPaginatedDict, getSalesList, getSaleItemsList
from website import db
from sqlalchemy import or_
from decimal import *

sale = Blueprint('sale', __name__)

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
        .order_by(Sale.id.desc()).paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getSalesList(paginated_items.items), paginated_items))

@sale.route('/sales/<int:saleId>', methods=["GET"])
def getSaleDetails(saleId):
    sales = Sale.query.filter_by(id=saleId).all()
    return jsonify(getSalesList(sales)[0])