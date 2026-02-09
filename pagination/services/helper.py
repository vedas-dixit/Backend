# apply_filters(data, filters)
# apply_sort(data, sort_by, order)
# apply_pagination(data, page, limit)
# GET /items?status=completed&min_amount=500
# &sort_by=created_at&order=desc&page=1&limit=20
from store.db import store_data
from typing import List
from models.models import DataModel,Status,SortBy,Order

#filters: 
def apply_filter(data: List[DataModel], status: Status | None, sortby: SortBy, order: Order):
    newdata = data[:]
    reverse = (order == Order.desc)
    if status:
        newdata = [x for x in newdata if x.status == status]
    if sortby == SortBy.created_at:
        newdata.sort(
            key=lambda x: x.created_at,
            reverse=reverse,
        )
    else:
        newdata.sort(
            key=lambda x: x.amount,
            reverse=reverse
        )
    return newdata



#Cursor:

def encode_cursor_key():
    pass

def decode_cursor_key():
    pass