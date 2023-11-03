import decimal

Decimal = decimal.Decimal
TWOPLACES = Decimal(10) ** -2


def getTaxDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "taxName": item.tax_name,
        "taxAlias": item.tax_alias,
        "taxValue": Decimal(item.tax_value).quantize(TWOPLACES),
    }


def getTaxesList(items):
    return [getTaxDict(i) for i in items]
