from flask import Blueprint, request, jsonify, request, Response
from .models import Product
from .helpers import getProductsList
from . import db
import os
api = Blueprint('api', __name__)

@api.route('/api/products', methods=["POST"])
def createProduct():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]

    product = Product(name=name, description=description, price=price)

    db.session.add(product)
    db.session.commit()
    return Response(f"{Product} created successfully!", 200)

@api.route('/api/products', methods=["GET"])
def getProducts():
    products = Product.query.all()
    response = jsonify(getProductsList(products))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@api.route('/', methods=["GET"])
def test():

    return os.getcwd() + '\\website\\'