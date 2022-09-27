from flask import Blueprint, request, jsonify, request, Response
from website.models import Order, OrderItem, Product
from website.helpers import getProductsList, getPaginatedDict, getOrdersList
from datetime import datetime
from website import db
from sqlalchemy import or_

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
        product_query = Product.query.filter_by(id=product["id"]).one()
        order_item = OrderItem(
            order=order,
            product=product_query,
            quantity=product["quantity"],
        )
        
        db.session.add(order_item)

    db.session.commit()
    data = {
        "orderId": order.id
    }
    
    return jsonify(data), 200

@order.route('/orders', methods=["GET"])
def getOrders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search')

    if search:
        search = search.strip().replace('+', ' ')\
            .replace('%20', ' ')
    else: 
        search = "*"

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