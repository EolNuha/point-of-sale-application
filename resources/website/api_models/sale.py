from flask_restx import fields

from .. import swagger

# Define the fields for an individual sale item
sale_item = swagger.model(
    "SaleItem",
    {
        "change_amount": fields.Float,
        "customer_amount": fields.Float,
        "date_created": fields.String,
        "date_modified": fields.String,
        "gross_profit_amount": fields.Float,
        "id": fields.Integer,
        "is_regular": fields.Boolean,
        "net_profit_amount": fields.Float,
        "subtotal_amount": fields.Float,
        "total_amount": fields.Float,
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
                        "tax_alias": fields.String,
                        "tax_name": fields.String,
                        "tax_value": fields.Float,
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
        "purchased_price": fields.Float,
        "selling_price": fields.Float,
        "tax": fields.Integer,
    },
)

# Define the Swagger model for SaleItem
sale_item_model = swagger.model(
    "SaleItem",
    {
        "date_created": fields.String,
        "date_modified": fields.String,
        "id": fields.Integer,
        "price_without_tax": fields.Float,
        "product": fields.Nested(product_model),  # Nest the Product model
        "quantity": fields.Float,
        "tax_amount": fields.Float,
    },
)

# Define the Swagger model for User
user_model = swagger.model(
    "User",
    {
        "active": fields.Boolean,
        "date_created": fields.String,
        "date_modified": fields.String,
        "email": fields.String,
        "first_name": fields.String,
        "id": fields.Integer,
        "last_name": fields.String,
        "user_role": fields.String,
        "username": fields.String,
    },
)

# Define the Swagger model for the Sale
sale_model = swagger.model(
    "Sale",
    {
        "change_amount": fields.Float,
        "customer_amount": fields.Float,
        "date_created": fields.String,
        "date_modified": fields.String,
        "gross_profit_amount": fields.Float,
        "id": fields.Integer,
        "is_regular": fields.Boolean,
        "net_profit_amount": fields.Float,
        "sale_items": fields.List(
            fields.Nested(sale_item_model)
        ),  # Nest the SaleItem model
        "subtotal_amount": fields.Float,
        "taxes": fields.Raw,  # This will be further defined in the SalePagination model
        "total_amount": fields.Float,
        "user": fields.Nested(user_model),  # Nest the User model
    },
)

# Define the Swagger model for the taxes in SalePagination
tax_model = swagger.model(
    "Tax",
    {
        "tax_alias": fields.String,
        "tax_name": fields.String,
        "tax_value": fields.Float,
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
        "total_amount": fields.Float,
        "gross_profit_amount": fields.Float,
        "net_profit_amount": fields.Float,
        "subtotal_amount": fields.Float,
        "customer_amount": fields.Float,
        "change_amount": fields.Float,
        "is_regular": fields.Boolean,
        "taxes": fields.Raw,
        "sale_items": fields.List(fields.Raw),
        "user": fields.Raw,
        "date_created": fields.String,
        "date_modified": fields.String,
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
        "customer_amount": fields.Float,
        "change_amount": fields.Float,
        "is_regular": fields.Boolean,
    },
)
