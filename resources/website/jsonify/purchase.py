from .settings import getTaxesList
import decimal
Decimal = decimal.Decimal
FOURPLACES = Decimal(10) ** -4
TWOPLACES = Decimal(10) ** -2

def getPurchaseDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "totalAmount": Decimal(item.total_amount).quantize(TWOPLACES),
        "subTotalAmount": Decimal(item.subtotal_amount).quantize(TWOPLACES),
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getDailyPurchaseDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "totalAmount": Decimal(item.total_amount).quantize(TWOPLACES),
        "subTotalAmount": Decimal(item.subtotal_amount).quantize(TWOPLACES),
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
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "product": {
            "id": item.product_id,
            "name": item.product_name,
            "barcode": item.product_barcode,
            "stock": Decimal(item.product_stock).quantize(TWOPLACES),
            "tax": item.product_tax,
            "purchasedPriceWOTax": Decimal(item.product_purchased_price_wo_tax).quantize(TWOPLACES),
            "purchasedPrice": Decimal(item.product_purchased_price).quantize(TWOPLACES),
            "measure": item.product_measure,
            "sellingPrice": Decimal(item.product_selling_price).quantize(TWOPLACES),
        },
        "taxAmount": Decimal(item.tax_amount).quantize(TWOPLACES),
        "totalAmount":  Decimal(item.total_amount).quantize(TWOPLACES),
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getSellerDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
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
