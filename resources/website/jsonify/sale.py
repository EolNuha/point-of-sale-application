from .user import getUserDict
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
        "total_amount": Decimal(item.total_amount).quantize(TWOPLACES),
        "gross_profit_amount": Decimal(item.gross_profit_amount).quantize(TWOPLACES),
        "net_profit_amount": Decimal(item.net_profit_amount).quantize(TWOPLACES),
        "subtotal_amount": Decimal(item.subtotal_amount).quantize(TWOPLACES),
        "customer_amount": Decimal(item.customer_amount).quantize(TWOPLACES),
        "change_amount": Decimal(item.change_amount).quantize(TWOPLACES),
        "is_regular": item.is_regular,
        "date_created": item.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%d.%m.%Y, %H:%M:%S"),
    }


def getDailySaleDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "total_amount": Decimal(item.total_amount).quantize(TWOPLACES),
        "gross_profit_amount": Decimal(item.gross_profit_amount).quantize(TWOPLACES),
        "net_profit_amount": Decimal(item.net_profit_amount).quantize(TWOPLACES),
        "subtotal_amount": Decimal(item.subtotal_amount).quantize(TWOPLACES),
        "customer_amount": Decimal(item.customer_amount).quantize(TWOPLACES),
        "change_amount": Decimal(item.change_amount).quantize(TWOPLACES),
        "is_regular": item.is_regular,
        "taxes": getGroupedByAliasTaxes(item.sale_taxes),
        "sale_items": getSaleItemsList(item.sale_items),
        "user": getUserDict(item.user),
        "date_created": item.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%d.%m.%Y, %H:%M:%S"),
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
            "purchased_price": float(
                Decimal(item.product_purchased_price).quantize(TWOPLACES)
            ),
            "selling_price": float(
                Decimal(item.product_selling_price).quantize(TWOPLACES)
            ),
        },
        "quantity": float(Decimal(item.product_quantity).quantize(TWOPLACES)),
        "price_without_tax": float(Decimal(item.price_without_tax).quantize(TWOPLACES)),
        "tax_amount": float(
            Decimal(item.tax_amount * item.product_quantity).quantize(TWOPLACES)
        ),
        "date_created": item.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%d.%m.%Y, %H:%M:%S"),
    }


def getSaleItemsList(items):
    return [getSaleItemDict(i) for i in items]


def getSalesList(sales):
    return [getSaleDict(i) for i in sales]


def getDailySalesList(sales):
    return [getDailySaleDict(i) for i in sales]


def getGroupedByAliasTaxes(data):
    result = defaultdict(lambda: {"tax_value": 0})
    for item in data:
        tax_alias = item.tax_alias
        tax_value = item.tax_value or 0
        result[tax_alias]["tax_value"] = Decimal(
            Decimal(result[tax_alias]["tax_value"]) + tax_value
        ).quantize(TWOPLACES)
        result[tax_alias]["tax_value"] = str(result[tax_alias]["tax_value"])

    return result
