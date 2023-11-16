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
        "stock": float(Decimal(item.stock).quantize(TWOPLACES)),
        "tax": item.tax,
        "purchased_price_wo_tax": float(
            Decimal(item.purchased_price_wo_tax).quantize(TWOPLACES)
        ),
        "purchased_price": float(Decimal(item.purchased_price).quantize(TWOPLACES)),
        "selling_price": float(Decimal(item.selling_price).quantize(TWOPLACES)),
        "expiration_date": item.expiration_date.strftime("%Y-%m-%d")
        if item.expiration_date
        else None,
        "date_created": item.date_created.strftime("%Y-%m-%d, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%Y-%m-%d, %H:%M:%S"),
    }


def getProductsList(products):
    return [getProductsDict(i) for i in products]
