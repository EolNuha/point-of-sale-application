from flask import Blueprint, request, jsonify, request
from website.models import Product
from website.helpers import getPaginatedDict
from website.json import getProductsList
from datetime import datetime
from website import db
from sqlalchemy import or_

product = Blueprint('product', __name__)

@product.route('/products', methods=["POST"])
def createProduct():
    name = request.json["name"]
    barcode = request.json["barcode"]
    stock = request.json["stock"]
    tax = request.json["tax"]
    purchased_price = request.json["purchasedPrice"]
    selling_price = request.json["sellingPrice"]

    product = Product(
        name=name.lower(), 
        barcode=barcode, 
        stock=stock, 
        tax=tax, 
        purchased_price=purchased_price, 
        selling_price=selling_price,
        date_created=datetime.now(),
        date_modified=datetime.now(),
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
    search = request.args.get('search', '*', type=str)

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

@product.route('/products/barcode/<int:barcode>', methods=["GET"])
def getProductDetailsByBarcode(barcode):
    product = Product.query.filter_by(barcode=barcode).first_or_404()
    return jsonify(getProductsList([product, product])[0])

@product.route('/products/<int:productId>', methods=["POST"])
def updateProductDetails(productId):
    name = request.json["name"]
    barcode = request.json["barcode"]
    stock = request.json["stock"]
    tax = request.json["tax"]
    purchased_price = request.json["purchasedPrice"]
    selling_price = request.json["sellingPrice"]
    
    product = Product.query.filter_by(id=productId).first_or_404()

    product.name = name
    product.barcode = barcode
    product.stock = stock
    product.tax = tax
    product.purchased_price = purchased_price
    product.selling_price = selling_price
    product.modified = datetime.now()

    db.session.commit()
    return "Success", 200

@product.route('/products/<int:productId>', methods=["DELETE"])
def deleteProductDetails(productId):
    Product.query.filter_by(id=productId).delete()
    db.session.commit()
    return "Success", 200


@product.route('/products/demo', methods=["GET"])
def createDemoProducts():
    demo = [
        ["test 1", "100100100", 100, 8, 1.5, 2],
        ["test 2", "100200100", 100, 18, 15, 18],
        ["test 3", "100300100", 100, 18, 5, 7.5],
        ["test 4", "100400100", 100, 8, 1.2, 1.6],
        ["test 5", "100500100", 100, 8, 1.5, 2],
        ["test 6", "100600100", 100, 8, 3, 4],
        ["test 7", "100700100", 100, 18, 20, 25],
        ["test 8", "100800100", 100, 18, 3.4, 4],
        ["test 9", "100900100", 100, 8, 4.5, 6],
        ["test 10", "1001000100", 100, 8, 1.5, 2],
    ]
    for i in demo:
        db.session.add( Product(
            name=i[0], 
            barcode=i[1], 
            stock=i[2], 
            tax=i[3], 
            purchased_price=i[4], 
            selling_price=i[5],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            ))
        db.session.commit()
    return "success", 200