def get_page_range(page, total, show=5):
    start = max((page - (show // 2)), 1)
    stop = min(start + show, total) + 1
    start = max(min(start, stop - show), 1)
    return list(range(start, stop)[:show])

def getProductsList(products):
    products_list = []
    for i in products:
        product_dict = {
            "id": i.id,
            "name": i.name,
            "barcode": i.barcode,
            "stock": i.stock,
            "purchasedPrice": i.purchased_price,
            "sellingPrice": i.selling_price,
            "dateCreated": i.date_created.strftime('%d-%m-%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d-%m-%Y, %H:%M:%S'),
        }
        products_list.append(product_dict)
    return products_list

def getOrdersList(orders):
    orders_list = []
    for i in orders:
        order_dict = {
            "id": i.id,
            "totalAmount": i.total_amount,
            "customerAmount": i.customer_amount,
            "changeAmount": i.change_amount,
            "dateCreated": i.date_created.strftime('%d-%m-%Y, %H:%M:%S'),
            "dateModified": i.date_modified.strftime('%d-%m-%Y, %H:%M:%S'),
        }
        orders_list.append(order_dict)
    return orders_list

def getPaginatedDict(data, paginated_items):
    return {
        "data": data,
        "pagination": {
            "has_next": paginated_items.has_next,
            "has_prev": paginated_items.has_prev,
            "page": paginated_items.page,
            "per_page": paginated_items.per_page,
            "pages": paginated_items.pages,
            "next_num": paginated_items.next_num,
            "prev_num": paginated_items.prev_num,
            "items": len(paginated_items.items),
            "total": paginated_items.total,
            "page_range": get_page_range(paginated_items.page, paginated_items.pages, 5)
        },
        
    }
