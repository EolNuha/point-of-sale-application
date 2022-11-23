from .user import getUserDict
from .settings import getTaxesList

def getSaleDict(item):
    return {
        "id": item.id,
        "totalAmount": item.total_amount,
        "subTotalAmount": item.subtotal_amount,
        "customerAmount": item.customer_amount,
        "changeAmount": item.change_amount,
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getDailySaleDict(item):
    return {
        "id": item.id,
        "totalAmount": item.total_amount,
        "subTotalAmount": item.subtotal_amount,
        "customerAmount": item.customer_amount,
        "changeAmount": item.change_amount,
        "taxes": getTaxesList(item.sale_taxes),
        "saleItems": getSaleItemsList(item.sale_items),
        "user": getUserDict(item.user),
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getSaleItemDict(item):
    return {
        "id": item.id,
        "product": {
            "id": item.product_id,
            "name": item.product_name,
            "barcode": item.product_barcode,
            "tax": item.product_tax,
            "purchasedPrice": item.product_purchased_price,
            "sellingPrice": item.product_selling_price,
        },
        "quantity": item.product_quantity,
        "priceWithoutTax": item.price_without_tax,
        "taxAmount": item.tax_amount,
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getSaleItemsList(items):
    return [getSaleItemDict(i) for i in items]

def getSalesList(sales):
    return [getSaleDict(i) for i in sales]

def getDailySalesList(sales):
    return [getDailySaleDict(i) for i in sales]