import decimal
from collections import defaultdict
import json

Decimal = decimal.Decimal
FOURPLACES = Decimal(10) ** -4
TWOPLACES = Decimal(10) ** -2


def getPurchaseDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "total_amount": Decimal(item.total_amount or 0).quantize(TWOPLACES),
        "subtotal_amount": Decimal(item.subtotal_amount or 0).quantize(TWOPLACES),
        "rabat_amount": Decimal(item.rabat_amount or 0).quantize(TWOPLACES),
        "total_tax_amount": Decimal(item.total_amount - item.subtotal_amount).quantize(
            TWOPLACES
        ),
        "date_created": item.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%d.%m.%Y, %H:%M:%S"),
    }


def getPurchaseDictExcel(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "date": item.date_created.strftime("%d.%m.%Y"),
        "id": item.id,
        "rabat_amount": Decimal(item.rabat_amount or 0).quantize(TWOPLACES),
        "subtotal_amount": Decimal(item.subtotal_amount or 0).quantize(TWOPLACES),
        "total_amount": Decimal(item.total_amount or 0).quantize(TWOPLACES),
        "total_tax_amount": Decimal(item.total_amount - item.subtotal_amount).quantize(
            TWOPLACES
        ),
    }


def getDailyPurchaseDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "total_amount": Decimal(item.total_amount or 0).quantize(TWOPLACES),
        "subtotal_amount": Decimal(item.subtotal_amount or 0).quantize(TWOPLACES),
        "rabat_amount": Decimal(item.rabat_amount or 0).quantize(TWOPLACES),
        "total_tax_amount": Decimal(item.total_amount - item.subtotal_amount).quantize(
            TWOPLACES
        ),
        "seller_name": item.seller_name,
        "seller_invoice_number": item.seller_invoice_number,
        "seller_fiscal_number": item.seller_fiscal_number,
        "seller_tax_number": item.seller_tax_number,
        "purchase_items": getPurchaseItemsList(item.purchase_items),
        "taxes": getGroupedByAliasTaxes(item.purchase_taxes),
        "date_created": item.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%d.%m.%Y, %H:%M:%S"),
    }


def getDailyPurchaseDictExcel(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    data = {
        "date": item.date_created.strftime("%d.%m.%Y"),
        "id": item.id,
        "seller_name": item.seller_name,
        "seller_invoice_number": item.seller_invoice_number,
        "seller_fiscal_number": item.seller_fiscal_number,
        "seller_tax_number": item.seller_tax_number,
        "rabat_amount": Decimal(item.rabat_amount or 0).quantize(TWOPLACES),
        "subtotal_amount": Decimal(item.subtotal_amount or 0).quantize(TWOPLACES),
        "total_amount": Decimal(item.total_amount or 0).quantize(TWOPLACES),
        "total_tax_amount": Decimal(item.total_amount - item.subtotal_amount).quantize(
            TWOPLACES
        ),
    }
    for tax in item.purchase_taxes:
        data[f"{tax.tax_name}%"] = tax.tax_value
    return data


def getPurchaseItemDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "product": {
            "id": item.product_id,
            "name": item.product_name,
            "barcode": item.product_barcode,
            "stock": str(Decimal(item.product_stock).quantize(TWOPLACES)),
            "tax": item.product_tax,
            "purchased_price_wo_tax": str(
                Decimal(item.product_purchased_price_wo_tax or 0).quantize(TWOPLACES)
            ),
            "purchased_price": str(
                Decimal(item.product_purchased_price or 0).quantize(TWOPLACES)
            ),
            "measure": item.product_measure,
            "selling_price": str(
                Decimal(item.product_selling_price or 0).quantize(TWOPLACES)
            ),
        },
        "tax_amount": str(
            Decimal(item.tax_amount * item.product_stock).quantize(TWOPLACES)
        ),
        "total_amount": str(Decimal(item.total_amount or 0).quantize(TWOPLACES)),
        "date_created": item.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%d.%m.%Y, %H:%M:%S"),
    }


def getSellerDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "seller_name": item.seller_name,
        "seller_invoice_number": item.seller_invoice_number,
        "seller_fiscal_number": item.seller_fiscal_number,
        "seller_tax_number": item.seller_tax_number,
        "date_created": item.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
        "date_modified": item.date_modified.strftime("%d.%m.%Y, %H:%M:%S"),
    }


def getTaxDict(item):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    return {
        "id": item.id,
        "tax_name": item.tax_name,
        "tax_alias": item.tax_alias,
        "tax_value": Decimal(item.tax_value or 0).quantize(TWOPLACES),
        "total_without_tax": Decimal(item.total_without_tax or 0).quantize(TWOPLACES),
    }


def getPurchaseItemsList(items):
    return [getPurchaseItemDict(i) for i in items]


def getDailyPurchasesList(items):
    return [getDailyPurchaseDict(i) for i in items]


def getDailyPurchasesListExcel(items):
    return [getDailyPurchaseDictExcel(i) for i in items]


def getPurchasesList(purchases):
    return [getPurchaseDict(i) for i in purchases]


def getPurchasesListExcel(purchases):
    return [getPurchaseDictExcel(i) for i in purchases]


def getSellersList(sellers):
    return [getSellerDict(i) for i in sellers]


def getTaxesList(items):
    return [getTaxDict(i) for i in items]


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))


def getGroupedByAliasTaxes(data):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    result = defaultdict(lambda: {"tax_value": 0, "total_without_tax": 0})

    for item in data:
        tax_alias = item.tax_alias
        tax_value = Decimal(item.tax_value or 0).quantize(TWOPLACES)
        total_without_tax = Decimal(item.total_without_tax or 0).quantize(TWOPLACES)
        result[tax_alias]["tax_value"] += tax_value
        result[tax_alias]["total_without_tax"] += total_without_tax

    return json.loads(json.dumps(result, default=decimal_default))
