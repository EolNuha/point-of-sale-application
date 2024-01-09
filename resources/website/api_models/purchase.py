from flask_restx import fields

from .. import swagger

taxes = swagger.model(
    "Taxes",
    {
        "id": fields.Integer,
        "tax_alias": fields.String,
        "tax_name": fields.String,
        "tax_value": fields.Float,
        "total_without_tax": fields.Float,
    },
)

grouped_purchases = swagger.model(
    "GroupedPurchases",
    {
        "date_created": fields.String,
        "date_modified": fields.String,
        "id": fields.Integer,
        "rabat_amount": fields.Float,
        "subtotal_amount": fields.Float,
        "total_amount": fields.Float,
        "total_tax_amount": fields.Float,
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
        "date_created": fields.String,
        "date_modified": fields.String,
        "id": fields.Integer,
        "tax_amount": fields.Float,
        "total_amount": fields.Float,
        "product": fields.Raw,
    },
)


detailed_purchases = swagger.model(
    "DetailedPurchases",
    {
        "date_created": fields.String,
        "date_modified": fields.String,
        "id": fields.Integer,
        "rabat_amount": fields.Float,
        "subtotal_amount": fields.Float,
        "total_amount": fields.Float,
        "total_tax_amount": fields.Float,
        "seller_fiscal_number": fields.Integer,
        "seller_tax_number": fields.String,
        "seller_invoice_number": fields.String,
        "seller_name": fields.String,
        "purchase_items": fields.List(fields.Nested(purchases_item)),
        "taxes": fields.Raw,
        "purchase_type": fields.String,
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
        "date_created": fields.String,
        "date_modified": fields.String,
        "id": fields.Integer,
        "seller_fiscal_number": fields.Integer,
        "seller_tax_number": fields.String,
        "seller_invoice_number": fields.String,
        "seller_name": fields.String,
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
        "purchase_items": fields.List(fields.Raw),
    },
)

purchase_create = swagger.model(
    "PurchaseCreate",
    {
        "products": fields.List(fields.Raw),
        "seller": fields.Raw,
    },
)
