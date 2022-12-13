def getProductsDict(item):
    return {
        "id": item.id,
        "name": item.name,
        "barcode": item.barcode,
        "stock": item.stock,
        "tax": item.tax,
        "purchasedPrice": item.purchased_price,
        "sellingPrice": item.selling_price,
        "expirationDate": item.expiration_date.strftime('%Y-%m-%d') if item.expiration_date else None,
        "dateCreated": item.date_created.strftime('%Y-%m-%d, %H:%M:%S'),
        "dateModified": item.date_modified.strftime('%Y-%m-%d, %H:%M:%S'),
    }

def getProductsList(products):
    return [getProductsDict(i) for i in products]