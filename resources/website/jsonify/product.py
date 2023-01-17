
import decimal
Decimal = decimal.Decimal
FOURPLACES = Decimal(10) ** -4
TWOPLACES = Decimal(10) ** -2
def getProductsDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "name": item.name,
        "barcode": item.barcode,
        "measure": item.measure,
        "stock": Decimal(item.stock).quantize(TWOPLACES),
        "tax": item.tax,
        "purchasedPriceWOTax": Decimal(item.purchased_price_wo_tax).quantize(TWOPLACES),
        "purchasedPrice": Decimal(item.purchased_price).quantize(TWOPLACES),
        "sellingPrice": Decimal(item.selling_price).quantize(TWOPLACES),
        "expirationDate": item.expiration_date.strftime('%Y-%m-%d') if item.expiration_date else None,
        "dateCreated": item.date_created.strftime('%Y-%m-%d, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%Y-%m-%d, %H:%M:%S'),
    }

def getProductsList(products):
    return [getProductsDict(i) for i in products]