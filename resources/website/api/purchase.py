from flask import Blueprint, request, jsonify, request
from website.models import Purchase, PurchaseItem, Product
from website.helpers import getPaginatedDict, getPurchasesList, getPurchaseItemsList
from website import db
from sqlalchemy import or_
from decimal import *

purchase = Blueprint('purchase', __name__)

@purchase.route('/purchases', methods=["POST"])
def createPurchase():
    products = request.json["products"]
    seller = request.json["seller"]
    total_amount = request.json["totalAmount"]

    purchase = Purchase(
        total_amount=total_amount,
            seller_name=seller["sellerName"],
            seller_invoice_number=seller["invoiceNumber"],
            seller_fiscal_number=seller["fiscalNumber"],
            seller_tax_number=seller["taxNumber"],
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
                tax_amount=tax_amount
            )

            product_query.name = product["productName"]
            product_query.tax = product["tax"]
            product_query.purchased_price = product["purchasedPrice"]
            product_query.selling_price = product["sellingPrice"]
            product_query.stock += Decimal(product["stock"])
        else:
            created_product = Product(
                name=product["productName"], 
                barcode=product["barcode"], 
                stock=product["stock"], 
                tax=product["tax"], 
                purchased_price=product["purchasedPrice"], 
                selling_price= product["sellingPrice"]
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
                tax_amount=tax_amount
            )
        db.session.add(purchase_item)

    subtotal, eight, eighteen = [], [], []

    for item in getPurchaseItemsList(purchase.purchase_items):
        subtotal.append(item['priceWithoutTax'] * Decimal(item['product']['stock']))
        if item['product']['tax'] == 8:
            eight.append(item['taxAmount'] * Decimal(item['product']['stock']))
        if item['product']['tax'] == 18:
            eighteen.append(item['taxAmount'] * Decimal(item['product']['stock']))
    
    purchase.subtotal_amount = sum(subtotal)
    purchase.eight_tax_amount = sum(eight)
    purchase.eighteen_tax_amount = sum(eighteen)
    
    db.session.commit()
    
    return jsonify("Success"), 200

@purchase.route('/purchases', methods=["GET"])
def getPurchases():
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
        ))\
        .order_by(Purchase.id.desc()).paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getPurchasesList(paginated_items.items), paginated_items))
