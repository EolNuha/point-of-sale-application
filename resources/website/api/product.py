from flask import Blueprint, request, jsonify, request, Response
from website.models import Product
from website.helpers import getProductsList
from datetime import datetime
from website import db

product = Blueprint('product', __name__)

@product.route('/products', methods=["POST"])
def createProduct():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]

    product = Product(name=name, description=description, price=price)

    db.session.add(product)
    db.session.commit()
    data = {
        "productId": product.id 
    }
    return jsonify(data), 200

@product.route('/products', methods=["GET"])
def getProducts():
    products = Product.query.all()
    response = jsonify(getProductsList(products))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

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