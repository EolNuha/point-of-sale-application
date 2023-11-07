from flask_restx import fields

from .. import swagger

# Define the fields for an individual sale item
sale_item = swagger.model(
    "SaleItem",
    {
        "changeAmount": fields.Float,
        "customerAmount": fields.Float,
        "dateCreated": fields.String,
        "dateModified": fields.String,
        "grossProfitAmount": fields.Float,
        "id": fields.Integer,
        "isRegular": fields.Boolean,
        "netProfitAmount": fields.Float,
        "subTotalAmount": fields.Float,
        "totalAmount": fields.Float,
        "taxes": fields.List(fields.Raw),
    },
)

# Define the sale_pagination model
sale_pagination = swagger.model(
    "SalePagination",
    {
        "page": fields.Integer,
        "per_page": fields.Integer,
        "pages": fields.Integer,
        "total": fields.Integer,
        "items": fields.Integer,
        "prev_num": fields.String,
        "next_num": fields.String,
        "has_next": fields.Boolean,
        "has_prev": fields.Boolean,
        "page_range": fields.List(fields.Integer),
        "salesSubTotalAmount": fields.Float,
        "salesTotalAmount": fields.Float,
        "salesTotalGrossProfit": fields.Float,
        "salesTotalNetProfit": fields.Float,
        "taxes": fields.List(
            fields.Nested(
                swagger.model(
                    "TaxItem",
                    {
                        "id": fields.Integer,
                        "taxAlias": fields.String,
                        "taxName": fields.String,
                        "taxValue": fields.Float,
                    },
                )
            ),
        ),
    },
)

# Define the sale model
sale = swagger.model(
    "SaleModel",
    {
        "data": fields.List(fields.Nested(sale_item)),
        "pagination": fields.Nested(sale_pagination),
    },
)


# Define the Swagger model for the Product
product_model = swagger.model(
    "Product",
    {
        "barcode": fields.Integer,
        "id": fields.Integer,
        "measure": fields.String,
        "name": fields.String,
        "purchasedPrice": fields.Float,
        "sellingPrice": fields.Float,
        "tax": fields.Integer,
    },
)

# Define the Swagger model for SaleItem
sale_item_model = swagger.model(
    "SaleItem",
    {
        "dateCreated": fields.String,
        "dateModified": fields.String,
        "id": fields.Integer,
        "priceWithoutTax": fields.Float,
        "product": fields.Nested(product_model),  # Nest the Product model
        "quantity": fields.Float,
        "taxAmount": fields.Float,
    },
)

# Define the Swagger model for User
user_model = swagger.model(
    "User",
    {
        "active": fields.Boolean,
        "dateCreated": fields.String,
        "dateModified": fields.String,
        "email": fields.String,
        "firstName": fields.String,
        "id": fields.Integer,
        "lastName": fields.String,
        "userRole": fields.String,
        "username": fields.String,
    },
)

# Define the Swagger model for the Sale
sale_model = swagger.model(
    "Sale",
    {
        "changeAmount": fields.Float,
        "customerAmount": fields.Float,
        "dateCreated": fields.String,
        "dateModified": fields.String,
        "grossProfitAmount": fields.Float,
        "id": fields.Integer,
        "isRegular": fields.Boolean,
        "netProfitAmount": fields.Float,
        "saleItems": fields.List(
            fields.Nested(sale_item_model)
        ),  # Nest the SaleItem model
        "subTotalAmount": fields.Float,
        "taxes": fields.Raw,  # This will be further defined in the SalePagination model
        "totalAmount": fields.Float,
        "user": fields.Nested(user_model),  # Nest the User model
    },
)

# Define the Swagger model for the taxes in SalePagination
tax_model = swagger.model(
    "Tax",
    {
        "taxAlias": fields.String,
        "taxName": fields.String,
        "taxValue": fields.Float,
    },
)

# Define the Swagger model for SalePagination
sale_pagination_model = swagger.model(
    "SalePagination",
    {
        "has_next": fields.Boolean,
        "has_prev": fields.Boolean,
        "items": fields.Integer,
        "next_num": fields.Integer,  # Define this structure if needed
        "page": fields.Integer,
        "page_range": fields.List(fields.Integer),
        "pages": fields.Integer,
        "per_page": fields.Integer,
        "prev_num": fields.Integer,  # Define this structure if needed
        "salesSubTotalAmount": fields.Float,
        "salesTotalAmount": fields.Float,
        "salesTotalGrossProfit": fields.Float,
        "salesTotalNetProfit": fields.Float,
        "taxes": fields.List(fields.Nested(tax_model)),  # Nest the Tax model
        "total": fields.Integer,
    },
)

# Define the Swagger model for the complete JSON structure
complete_model = swagger.model(
    "CompleteModel",
    {
        "data": fields.List(fields.Nested(sale_model)),  # Nest the Sale model
        "pagination": fields.Nested(
            sale_pagination_model
        ),  # Nest the SalePagination model
    },
)

sale_details_model = swagger.model(
    "SaleDetails",
    {
        "id": fields.Integer,
        "totalAmount": fields.Float,
        "grossProfitAmount": fields.Float,
        "netProfitAmount": fields.Float,
        "subTotalAmount": fields.Float,
        "customerAmount": fields.Float,
        "changeAmount": fields.Float,
        "isRegular": fields.Boolean,
        "taxes": fields.Raw,
        "saleItems": fields.List(fields.Raw),
        "user": fields.Raw,
        "dateCreated": fields.String,
        "dateModified": fields.String,
    },
)

sale_update_model = swagger.model(
    "SaleUpdate",
    {
        "deleted_items": fields.List(fields.Raw),
        "sale_items": fields.List(fields.Raw),
    },
)

sale_create_model = swagger.model(
    "SaleCreate",
    {
        "products": fields.List(fields.Raw),
        "customerAmount": fields.Float,
        "changeAmount": fields.Float,
        "isRegular": fields.Boolean,
    },
)
