from .user import getUserDict
from .settings import getTaxesList
from collections import defaultdict
import decimal
Decimal = decimal.Decimal
FOURPLACES = Decimal(10) ** -4
TWOPLACES = Decimal(10) ** -2
def getSaleDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "totalAmount": Decimal(item.total_amount).quantize(TWOPLACES),
        "grossProfitAmount": Decimal(item.gross_profit_amount).quantize(TWOPLACES),
        "netProfitAmount": Decimal(item.net_profit_amount).quantize(TWOPLACES),
        "subTotalAmount": Decimal(item.subtotal_amount).quantize(TWOPLACES),
        "customerAmount": Decimal(item.customer_amount).quantize(TWOPLACES),
        "changeAmount": Decimal(item.change_amount).quantize(TWOPLACES),
        "isRegular": item.is_regular,
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getDailySaleDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "totalAmount": Decimal(item.total_amount).quantize(TWOPLACES),
        "grossProfitAmount": Decimal(item.gross_profit_amount).quantize(TWOPLACES),
        "netProfitAmount": Decimal(item.net_profit_amount).quantize(TWOPLACES),
        "subTotalAmount": Decimal(item.subtotal_amount).quantize(TWOPLACES),
        "customerAmount": Decimal(item.customer_amount).quantize(TWOPLACES),
        "changeAmount": Decimal(item.change_amount).quantize(TWOPLACES),
        "isRegular": item.is_regular,
        "taxes": getGroupedByAliasTaxes(item.sale_taxes),
        "saleItems": getSaleItemsList(item.sale_items),
        "user": getUserDict(item.user),
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getSaleItemDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "product": {
            "id": item.product_id,
            "name": item.product_name,
            "barcode": item.product_barcode,
            "measure": item.product_measure,
            "tax": item.product_tax,
            "purchasedPrice": Decimal(item.product_purchased_price).quantize(TWOPLACES),
            "sellingPrice": Decimal(item.product_selling_price).quantize(TWOPLACES),
        },
        "quantity": Decimal(item.product_quantity).quantize(TWOPLACES),
        "priceWithoutTax": Decimal(item.price_without_tax).quantize(TWOPLACES),
        "taxAmount": Decimal(item.tax_amount * item.product_quantity).quantize(TWOPLACES),
        "dateCreated": item.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getSaleItemsList(items):
    return [getSaleItemDict(i) for i in items]

def getSalesList(sales):
    return [getSaleDict(i) for i in sales]

def getDailySalesList(sales):
    return [getDailySaleDict(i) for i in sales]

def getGroupedByAliasTaxes(data):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    result = defaultdict(lambda: {'taxValue': Decimal(0)})
    for item in data:
        tax_alias = item.tax_alias
        tax_value = Decimal(item.tax_value or 0).quantize(TWOPLACES)
        result[tax_alias]['taxValue'] += tax_value

    return result