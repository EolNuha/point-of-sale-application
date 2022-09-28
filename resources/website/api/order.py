from flask import Blueprint, request, jsonify, request
from website.models import Order, OrderItem, Product
from website.helpers import getPaginatedDict, getOrdersList, getOrderItemsList
from website import db
from sqlalchemy import or_
from decimal import *

order = Blueprint('order', __name__)

@order.route('/orders', methods=["POST"])
def createOrder():
    products = request.json["products"]
    total_amount = request.json["totalAmount"]
    customer_amount = request.json["customerAmount"]
    change_amount = request.json["changeAmount"]

    order = Order(
        total_amount=total_amount,
        customer_amount=customer_amount,
        change_amount=change_amount,
    )

    db.session.add(order)
    

    for product in products:
        decimal_price = Decimal(product["sellingPrice"])
        decimal_tax = Decimal(product["tax"])
        price_without_tax = decimal_price - (decimal_tax / 100) * decimal_price
        tax_amount = (decimal_tax / 100) * decimal_price

        product_query = Product.query.filter_by(id=product["id"]).one()
        order_item = OrderItem(
            order=order,
            product=product_query,
            quantity=Decimal(product["quantity"]),
            price_without_tax=price_without_tax,
            tax_amount=tax_amount
        )

        product_query.stock -= Decimal(product["quantity"])
        
        db.session.add(order_item)

    subtotal, eight, eighteen = [], [], []

    for item in getOrderItemsList(order.order_items):
        subtotal.append(item['priceWithoutTax'] * Decimal(item['quantity']))
        if item['product']['tax'] == 8:
            eight.append(item['taxAmount'] * Decimal(item['quantity']))
        if item['product']['tax'] == 18:
            eighteen.append(item['taxAmount'] * Decimal(item['quantity']))
    
    order.subtotal_amount = sum(subtotal)
    order.eight_tax_amount = sum(eight)
    order.eighteen_tax_amount = sum(eighteen)
    
    db.session.commit()
    data = {
        "orderId": order.id
    }
    
    return jsonify(data), 200

@order.route('/orders', methods=["GET"])
def getOrders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '*', type=str)

    if '*' in search or '_' in search: 
        looking_for = search.replace('_', '__')\
            .replace('*', '%')\
            .replace('?', '_')
    else:
        looking_for = '%{0}%'.format(search)
        
    paginated_items = Order.query.filter(or_(
        Order.id.ilike(looking_for),
        ))\
        .order_by(Order.id.desc()).paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getOrdersList(paginated_items.items), paginated_items))

@order.route('/orders/<int:orderId>', methods=["GET"])
def getOrderDetails(orderId):
    orders = Order.query.filter_by(id=orderId).all()
    return jsonify(getOrdersList(orders)[0])