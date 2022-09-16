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
            "description": i.description,
            "price": i.price,
            "date": i.date_created.strftime('%d-%m-%Y, %H:%M:%S'),
            "modified": i.modified.strftime('%d-%m-%Y, %H:%M:%S'),
        }
        products_list.append(product_dict)
    return products_list
