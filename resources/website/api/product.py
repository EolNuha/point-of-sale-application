from flask import Blueprint, request, jsonify, request, Response
from website.models.product import Product
from website.helpers import getPaginatedDict
from website.jsonify.product import getProductsList, getProductsDict
from datetime import datetime, date, time, timedelta
from website import db
from sqlalchemy import or_, asc, desc
import random

product_api = Blueprint('product_api', __name__)

@product_api.route('/products', methods=["POST"])
def createProduct():
    name = request.json["name"]
    barcode = request.json["barcode"]
    stock = request.json["stock"]
    tax = request.json["tax"]
    purchased_price = request.json["purchasedPrice"]
    selling_price = request.json["sellingPrice"]
    expiration_date = request.json["expirationDate"]
    measure = request.json["measure"]

    if expiration_date:
        expiration_date = expiration_date.split("-")
        expiration_date = datetime.combine(date(year=int(expiration_date[0]), month=int(expiration_date[1]), day=int(expiration_date[2])), time.min)
    else:
        expiration_date = None

    found_with_name = Product.query.filter_by(name=name).first()
    found_with_barcode = Product.query.filter_by(barcode=barcode).first()

    if found_with_name:
        return Response(response="productWithNameExists", status=500)
    if found_with_barcode:
        return Response(response="productWithBarcodeExists", status=500)


    product = Product(
        name=name, 
        barcode=barcode, 
        stock=stock, 
        tax=tax, 
        purchased_price=purchased_price, 
        selling_price=selling_price,
        measure=measure,
        expiration_date=expiration_date,
        date_created=datetime.now(),
        date_modified=datetime.now(),
        )

    db.session.add(product)
    db.session.commit()
    data = {
        "productId": product.id 
    }
    return jsonify(data), 200

@product_api.route('/products', methods=["GET"])
def getProducts():
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
        
    paginated_items = Product.query.filter(or_(
        Product.name.ilike(looking_for),
        Product.id.ilike(looking_for),
        Product.barcode.ilike(looking_for),
        ))\
        .order_by(sort).paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getProductsList(paginated_items.items), paginated_items))

@product_api.route('/products/<int:productId>', methods=["GET"])
def getProductDetails(productId):
    return jsonify(getProductsDict(Product.query.filter_by(id=productId).first_or_404()))

@product_api.route('/products/barcode/<int:barcode>', methods=["GET"])
def getProductDetailsByBarcode(barcode):
    return jsonify(getProductsDict(Product.query.filter_by(barcode=barcode).first_or_404()))

@product_api.route('/products/<int:productId>', methods=["POST"])
def updateProductDetails(productId):
    name = request.json["name"]
    barcode = request.json["barcode"]
    stock = request.json["stock"]
    tax = request.json["tax"]
    purchased_price_wo_tax = request.json["purchasedPriceWOTax"]
    purchased_price = request.json["purchasedPrice"]
    measure = request.json["measure"]
    selling_price = request.json["sellingPrice"]
    expiration_date = request.json["expirationDate"]

    if expiration_date:
        expiration_date = expiration_date.split("-")
        expiration_date = datetime.combine(date(year=int(expiration_date[0]), month=int(expiration_date[1]), day=int(expiration_date[2])), time.min)
    else:
        expiration_date = None
    
    product = Product.query.filter_by(id=productId).first_or_404()

    found_with_name = Product.query.filter_by(name=name).first()
    found_with_barcode = Product.query.filter_by(barcode=barcode).first()

    if found_with_name and name != product.name:
        return Response(response="productWithNameExists", status=500)
    if found_with_barcode and barcode != product.barcode:
        return Response(response="productWithBarcodeExists", status=500)

    product.name = name
    product.barcode = barcode
    product.stock = stock
    product.tax = tax
    product.purchased_price_wo_tax = purchased_price_wo_tax
    product.purchased_price = purchased_price
    product.selling_price = selling_price
    product.measure = measure
    product.expiration_date = expiration_date
    product.date_modified = datetime.now()

    db.session.commit()
    return "Success", 200

@product_api.route('/products/<int:productId>', methods=["DELETE"])
def deleteProductDetails(productId):
    Product.query.filter_by(id=productId).delete()
    db.session.commit()
    return "Success", 200

@product_api.route('/products', methods=["DELETE"])
def deleteProducts():
    products = request.json["products"]
    Product.query.filter(Product.id.in_(products)).delete()
    db.session.commit()
    return "Success", 200


@product_api.route('/products/demo', methods=["GET"])
def createDemoProducts():
    taxes = [8, 18]
    for i in range(2000, 5001):
        rand_price = round(random.uniform(0.2, 5), 2)
        db.session.add( Product(
            name=f"test product {i}", 
            barcode=int(f"1{i:09}"), 
            stock=100, 
            tax=taxes[random.randint(0, 1)], 
            purchased_price=rand_price, 
            selling_price=(rand_price + 1/10 * rand_price),
            expiration_date=datetime.now() + timedelta(days = random.randint(15, 100)),
            date_created=datetime.now(),
            date_modified=datetime.now(),
            ))
        db.session.commit()
    return "success", 200