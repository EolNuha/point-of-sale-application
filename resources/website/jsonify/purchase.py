from .settings import getTaxesList

def getPurchaseDict(item):
    return {
        "id": item.id,
        "totalAmount": item.total_amount,
        "subTotalAmount": item.subtotal_amount,
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getDailyPurchaseDict(item):
    return {
        "id": item.id,
        "totalAmount": item.total_amount,
        "subTotalAmount": item.subtotal_amount,
        "sellerName": item.seller_name,
        "sellerInvoiceNumber": item.seller_invoice_number,
        "sellerFiscalNumber": item.seller_fiscal_number,
        "sellerTaxNumber": item.seller_tax_number,
        "purchaseItems": getPurchaseItemsList(item.purchase_items),
        "taxes": getTaxesList(item.purchase_taxes),
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getPurchaseItemDict(item):
    return {
        "id": item.id,
        "product": {
            "id": item.product_id,
            "name": item.product_name,
            "barcode": item.product_barcode,
            "stock": item.product_stock,
            "tax": item.product_tax,
            "purchasedPrice": item.product_purchased_price,
            "sellingPrice": item.product_selling_price,
        },
        "priceWithoutTax": item.price_without_tax,
        "taxAmount": item.tax_amount,
        "totalAmount": item.total_amount,
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getSellerDict(item):
    return {
        "id": item.id,
        "sellerName": item.seller_name,
        "sellerInvoiceNumber": item.seller_invoice_number,
        "sellerFiscalNumber": item.seller_fiscal_number,
        "sellerTaxNumber": item.seller_tax_number,
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getPurchaseItemsList(items):
    return [getPurchaseItemDict(i) for i in items]

def getDailyPurchasesList(items):
    return [getDailyPurchaseDict(i) for i in items]

def getPurchasesList(purchases):
    return [getPurchaseDict(i) for i in purchases]

def getSellersList(sellers):
    return [getSellerDict(i) for i in sellers]
