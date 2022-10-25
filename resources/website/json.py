def getUserDict(user):
    return {
        "id": user.id,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "username": user.username,
        "userType": user.user_type,
        "email": user.email,
        "dateCreated": user.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
        "dateModified": user.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
    }

def getUsersList(users):
    users_list = []
    for i in users:
        user_dict = {
            "id": i.id,
            "firstName": i.first_name,
            "lastName": i.last_name,
            "username": i.username,
            "userType": i.user_type,
            "email": i.email,
            "dateCreated": i.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
        }
        users_list.append(user_dict)
    return users_list

def getProductsList(products):
    products_list = []
    for i in products:
        product_dict = {
            "id": i.id,
            "name": i.name,
            "barcode": i.barcode,
            "stock": i.stock,
            "tax": i.tax,
            "purchasedPrice": i.purchased_price,
            "sellingPrice": i.selling_price,
            "dateCreated": i.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
        }
        products_list.append(product_dict)
    return products_list

def getSaleItemsList(items):
    sales_list = []
    for i in items:
        sale_dict = {
            "id": i.id,
            "product": {
                "id": i.product_id,
                "name": i.product_name,
                "barcode": i.product_barcode,
                "tax": i.product_tax,
                "purchasedPrice": i.product_purchased_price,
                "sellingPrice": i.product_selling_price,
            },
            "quantity": i.product_quantity,
            "priceWithoutTax": i.price_without_tax,
            "taxAmount": i.tax_amount,
            "dateCreated": i.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
        }
        sales_list.append(sale_dict)
    return sales_list

def getSalesList(sales):
    sales_list = []
    for i in sales:
        sale_dict = {
            "id": i.id,
            "totalAmount": i.total_amount,
            "subTotalAmount": i.subtotal_amount,
            "eightTaxAmount": i.eight_tax_amount,
            "eighteenTaxAmount": i.eighteen_tax_amount,
            "customerAmount": i.customer_amount,
            "changeAmount": i.change_amount,
            "dateCreated": i.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
        }
        sales_list.append(sale_dict)
    return sales_list

def getDailySalesList(sales):
    sales_list = []
    for i in sales:
        sale_dict = {
            "id": i.id,
            "totalAmount": i.total_amount,
            "subTotalAmount": i.subtotal_amount,
            "eightTaxAmount": i.eight_tax_amount,
            "eighteenTaxAmount": i.eighteen_tax_amount,
            "customerAmount": i.customer_amount,
            "changeAmount": i.change_amount,
            "user": getUserDict(i.user),
            "dateCreated": i.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
        }
        sales_list.append(sale_dict)
    return sales_list

def getPurchaseItemsList(items):
    purchases_list = []
    for i in items:
        purchase_dict = {
            "id": i.id,
            "product": {
                "id": i.product_id,
                "name": i.product_name,
                "barcode": i.product_barcode,
                "stock": i.product_stock,
                "tax": i.product_tax,
                "purchasedPrice": i.product_purchased_price,
                "sellingPrice": i.product_selling_price,
            },
            "priceWithoutTax": i.price_without_tax,
            "taxAmount": i.tax_amount,
            "totalAmount": i.total_amount,
            "dateCreated": i.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
        }
        purchases_list.append(purchase_dict)
    return purchases_list

def getPurchasesList(purchases):
    purchases_list = []
    for i in purchases:
        purchase_dict = {
            "id": i.id,
            "sellerName": i.seller_name,
            "sellerInvoiceNumber": i.seller_invoice_number,
            "sellerFiscalNumber": i.seller_fiscal_number,
            "sellerTaxNumber": i.seller_tax_number,
            "totalAmount": i.total_amount,
            "subTotalAmount": i.subtotal_amount,
            "eightTaxAmount": i.eight_tax_amount,
            "eighteenTaxAmount": i.eighteen_tax_amount,
            "purchaseItems": getPurchaseItemsList(i.purchase_items),
            "user": getUserDict(i.user),
            "dateCreated": i.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
        }
        purchases_list.append(purchase_dict)
    return purchases_list

def getSellersList(sellers):
    sellers_list = []
    for i in sellers:
        seller_dict = {
            "id": i.id,
            "sellerName": i.seller_name,
            "sellerInvoiceNumber": i.seller_invoice_number,
            "sellerFiscalNumber": i.seller_fiscal_number,
            "sellerTaxNumber": i.seller_tax_number,
            "dateCreated": i.date_created.strftime('%d.%m.%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d.%m.%Y, %H:%M:%S'),
        }
        sellers_list.append(seller_dict)
    return sellers_list
