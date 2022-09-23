from flask import Blueprint, request, jsonify, request, Response
from website.models import Product
from website.helpers import getProductsList, getPaginatedDict
from datetime import datetime
from website import db
from sqlalchemy import or_

product = Blueprint('product', __name__)

@product.route('/products', methods=["POST"])
def createProduct():
    name = request.json["name"]
    barcode = request.json["barcode"]
    stock = request.json["stock"]
    purchased_price = request.json["purchasedPrice"]
    selling_price = request.json["sellingPrice"]

    product = Product(
        name=name, 
        barcode=barcode, 
        stock=stock, 
        purchased_price=purchased_price, 
        selling_price=selling_price
        )

    db.session.add(product)
    db.session.commit()
    data = {
        "productId": product.id 
    }
    return jsonify(data), 200

@product.route('/products', methods=["GET"])
def getProducts():
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
        
    paginated_items = Product.query.filter(or_(
        Product.name.ilike(looking_for),
        Product.id.ilike(looking_for),
        Product.barcode.ilike(looking_for),
        ))\
        .order_by(Product.id.desc()).paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getProductsList(paginated_items.items), paginated_items))

@product.route('/products/<int:productId>', methods=["GET"])
def getProductDetails(productId):
    products = Product.query.filter_by(id=productId).all()
    return jsonify(getProductsList(products)[0])

@product.route('/products/<int:productId>', methods=["POST"])
def updateProductDetails(productId):
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    
    product = Product.query.filter_by(id=productId).first_or_404()

    product.name = name
    product.description = description
    product.price = price
    product.modified = datetime.now()

    db.session.commit()
    return "Success", 200

@product.route('/products/<int:productId>', methods=["DELETE"])
def deleteProductDetails(productId):
    product = Product.query.filter_by(id=productId).delete()
    db.session.commit()
    return "Success", 200