from flask_restx import fields

from .. import swagger

taxes = swagger.model(
    "Taxes",
    {
        "id": fields.Integer,
        "taxAlias": fields.String,
        "taxName": fields.String,
        "taxValue": fields.Float,
        "totalWithoutTax": fields.Float,
    },
)

grouped_purchases = swagger.model(
    "GroupedPurchases",
    {
        "dateCreated": fields.String,
        "dateModified": fields.String,
        "id": fields.Integer,
        "rabatAmount": fields.Float,
        "subTotalAmount": fields.Float,
        "totalAmount": fields.Float,
        "totalTaxAmount": fields.Float,
        "taxes": fields.List(fields.Nested(taxes)),
    },
)

purchase_pagination = swagger.model(
    "SalePagination",
    {
        "page": fields.Integer,
        "per_page": fields.Integer,
        "pages": fields.Integer,
        "total": fields.Integer,
        "items": fields.Integer,
        "prev_num": fields.Integer,
        "next_num": fields.Integer,
        "has_next": fields.Boolean,
        "has_prev": fields.Boolean,
        "page_range": fields.List(fields.Integer),
    },
)


grouped_purchases_data = swagger.model(
    "GroupedPurchasesData",
    {
        "data": fields.List(fields.Nested(grouped_purchases)),
        "pagination": fields.Nested(purchase_pagination),
    },
)

purchases_item = swagger.model(
    "PurchasesItem",
    {
        "dateCreated": fields.String,
        "dateModified": fields.String,
        "id": fields.Integer,
        "taxAmount": fields.Float,
        "totalAmount": fields.Float,
        "product": fields.Raw,
    },
)


detailed_purchases = swagger.model(
    "DetailedPurchases",
    {
        "dateCreated": fields.String,
        "dateModified": fields.String,
        "id": fields.Integer,
        "rabatAmount": fields.Float,
        "subTotalAmount": fields.Float,
        "totalAmount": fields.Float,
        "totalTaxAmount": fields.Float,
        "sellerFiscalNumber": fields.Integer,
        "sellerTaxNumber": fields.Integer,
        "sellerInvoiceNumber": fields.String,
        "sellerName": fields.String,
        "purchaseItems": fields.List(fields.Nested(purchases_item)),
        "taxes": fields.Raw,
    },
)


detailed_purchases_data = swagger.model(
    "DetailedPurchasesData",
    {
        "data": fields.List(fields.Nested(detailed_purchases)),
        "pagination": fields.Nested(purchase_pagination),
    },
)


sellers = swagger.model(
    "Sellers",
    {
        "dateCreated": fields.String,
        "dateModified": fields.String,
        "id": fields.Integer,
        "sellerFiscalNumber": fields.Integer,
        "sellerTaxNumber": fields.Integer,
        "sellerInvoiceNumber": fields.String,
        "sellerName": fields.String,
    },
)

sellers_data = swagger.model(
    "SellersData",
    {
        "data": fields.List(fields.Nested(sellers)),
        "pagination": fields.Nested(purchase_pagination),
    },
)


purchase_edit = swagger.model(
    "PurchaseEdit",
    {
        "deletedItems": fields.List(fields.Raw),
        "purchaseItems": fields.List(fields.Raw),
    },
)

purchase_create = swagger.model(
    "PurchaseCreate",
    {
        "products": fields.List(fields.Raw),
        "seller": fields.Raw,
    },
)
