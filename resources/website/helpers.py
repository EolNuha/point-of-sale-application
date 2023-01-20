
from decimal import *
import pandas as pd
from datetime import datetime, date, time, timedelta
from collections import Counter
import decimal
Decimal = decimal.Decimal
TWOPLACES = Decimal(10) ** -2

def get_page_range(page, total):
    if page < 4 or page in range(total - 2, total + 1): show = 5
    else: show = 3
    start = max((page - (show // 2)), 1)
    stop = min(start + show, total) + 1
    start = max(min(start, stop - show), 1)
    return list(range(start, stop)[:show])

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
            "page_range": get_page_range(paginated_items.page, paginated_items.pages)
        },
        
    }

def get_percentage_change(current, previous):
    if current == previous:
        return 0
    try:
        return format(((current - previous) / previous) * Decimal(100.00), ".2f")
    except ZeroDivisionError:
        return ""

def get_curr_prev_chart(date_start, date_end, curr, prev):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    date_ranges = pd.date_range(date_start, date_end)
    date_ranges = [d.strftime("%d/%m/%Y") for d in date_ranges]
    date_diff = abs((date_start - date_end).days)

    curr_incomp_series = []
    curr_comp_series = [0] * len(date_ranges)
    curr_options = []
    prev_incomp_series = []
    prev_comp_series = [0] * len(date_ranges)
    prev_options = []

    for item in curr:
        curr_options.append(item.date_created.strftime('%d/%m/%Y'))
        curr_incomp_series.append(Decimal(item.total_amount).quantize(TWOPLACES))

    for item in prev:
        option_date = item.date_created + timedelta(date_diff)
        prev_options.append(option_date.strftime('%d/%m/%Y'))
        prev_incomp_series.append(Decimal(item.total_amount).quantize(TWOPLACES))
    
    for index, d in enumerate(date_ranges):
        if d in curr_options:
            curr_idx = curr_options.index(d)
            curr_comp_series[index] = curr_incomp_series[curr_idx]
        if d in prev_options:
            prev_idx = prev_options.index(d)
            prev_comp_series[index] = prev_incomp_series[prev_idx]

    return {
        "curr_series": curr_comp_series,
        "prev_series": prev_comp_series,
        "options": date_ranges
    }

def get_curr_prev_dates(request):
    custom_start_date = request.args.get('startDate', type=str)
    custom_end_date = request.args.get('endDate', type=str)
    custom_start_date = custom_start_date.split("-")
    custom_end_date = custom_end_date.split("-")

    date_start = datetime.combine(date(year=int(custom_start_date[0]), month=int(custom_start_date[1]), day=int(custom_start_date[2])), time.min)
    date_end = datetime.combine(date(year=int(custom_end_date[0]), month=int(custom_end_date[1]), day=int(custom_end_date[2])), time.max)
    date_diff = abs((date_start - date_end).days)

    prev_date_start = date_start - timedelta(days=date_diff)
    prev_date_end = datetime.combine((date_start - timedelta(days=1)), time.max) 

    return {
        "date_start": date_start,
        "date_end": date_end,
        "prev_date_start": prev_date_start,
        "prev_date_end": prev_date_end,
    }

def sumListOfDicts(arr):
    my_dict = Counter()
    for d in arr:
        for key, value in d.items():
            my_dict[key] += value
    return dict(my_dict)