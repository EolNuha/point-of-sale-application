from flask_restx import fields

from .. import swagger

product_model = swagger.model("Product", {
    "id": fields.Integer,
    "barcode": fields.Integer,
    "name": fields.String,
    "stock": fields.Float,
    "tax": fields.Integer,
    "purchased_price_wo_tax": fields.Float,
    "purchased_price": fields.Float,
    "selling_price": fields.Float,
    "measure": fields.String,
    "expiration_date": fields.String,
    "date_created": fields.String,
    "date_modified": fields.String,
})

product_create_model = swagger.model("ProductCreate", {
    "barcode": fields.Integer,
    "name": fields.String,
    "stock": fields.Float,
    "tax": fields.Integer,
    "purchased_price_wo_tax": fields.Float,
    "purchased_price": fields.Float,
    "selling_price": fields.Float,
    "measure": fields.String,
    "expiration_date": fields.String,
})

products_delete_model = swagger.model("ProductsDelete", {
    "products": fields.List(fields.Integer),
})