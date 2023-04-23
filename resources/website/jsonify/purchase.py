import decimal
from collections import defaultdict
Decimal = decimal.Decimal
FOURPLACES = Decimal(10) ** -4
TWOPLACES = Decimal(10) ** -2

def getPurchaseDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "totalAmount": Decimal(item.total_amount or 0).quantize(TWOPLACES),
        "subTotalAmount": Decimal(item.subtotal_amount or 0).quantize(TWOPLACES),
        "rabatAmount": Decimal(item.rabat_amount or 0).quantize(TWOPLACES),
        "totalTaxAmount": Decimal(item.total_amount - item.subtotal_amount).quantize(TWOPLACES),
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getDailyPurchaseDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "totalAmount": Decimal(item.total_amount or 0).quantize(TWOPLACES),
        "subTotalAmount": Decimal(item.subtotal_amount or 0).quantize(TWOPLACES),
        "rabatAmount": Decimal(item.rabat_amount or 0).quantize(TWOPLACES),
        "totalTaxAmount": Decimal(item.total_amount - item.subtotal_amount).quantize(TWOPLACES),
        "sellerName": item.seller_name,
        "sellerInvoiceNumber": item.seller_invoice_number,
        "sellerFiscalNumber": item.seller_fiscal_number,
        "sellerTaxNumber": item.seller_tax_number,
        "purchaseItems": getPurchaseItemsList(item.purchase_items),
        "taxes": getGroupedByAliasTaxes(item.purchase_taxes),
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
            "purchasedPriceWOTax": Decimal(item.product_purchased_price_wo_tax or 0).quantize(TWOPLACES),
            "purchasedPrice": Decimal(item.product_purchased_price or 0).quantize(TWOPLACES),
            "measure": item.product_measure,
            "sellingPrice": Decimal(item.product_selling_price or 0).quantize(TWOPLACES),
        },
        "taxAmount": Decimal(item.tax_amount * item.product_stock).quantize(TWOPLACES),
        "totalAmount":  Decimal(item.total_amount or 0).quantize(TWOPLACES),
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

def getTaxDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "taxName": item.tax_name,
        "taxAlias": item.tax_alias,
        "taxValue": Decimal(item.tax_value or 0).quantize(TWOPLACES),
        "totalWithoutTax": Decimal(item.total_without_tax or 0).quantize(TWOPLACES),
    }

def getPurchaseItemsList(items):
    return [getPurchaseItemDict(i) for i in items]

def getDailyPurchasesList(items):
    return [getDailyPurchaseDict(i) for i in items]

def getPurchasesList(purchases):
    return [getPurchaseDict(i) for i in purchases]

def getSellersList(sellers):
    return [getSellerDict(i) for i in sellers]

def getTaxesList(items):
    return [getTaxDict(i) for i in items]

def getGroupedByAliasTaxes(data):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    result = defaultdict(lambda: {'taxValue': Decimal(0), 'totalWithoutTax': Decimal(0)})
    for item in data:
        tax_alias = item.tax_alias
        tax_value = Decimal(item.tax_value or 0).quantize(TWOPLACES)
        total_without_tax = Decimal(item.total_without_tax or 0).quantize(TWOPLACES)
        result[tax_alias]['taxValue'] += tax_value
        result[tax_alias]['totalWithoutTax'] += total_without_tax

    return result
