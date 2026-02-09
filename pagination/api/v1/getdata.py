from fastapi import APIRouter, Query
from store.db import store_data
from models.models import PaginatedResponse,Status,Order,SortBy
from services.helper import apply_filter
router = APIRouter()
import math
@router.get("/")
def get_items(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    status: Status | None = None,
    order: Order | None = Order.asc,
    sort: SortBy | None = SortBy.created_at,
):
        
    data = apply_filter(data=store_data,status=status,sortby=sort,order=order)
    st = (page - 1) * limit
    total_pages = math.ceil(len(store_data) / limit)
    total_items = math.ceil(len(data))
    paginated_data = data[st:(st+limit)]
    return PaginatedResponse(
        page=page,
        data=paginated_data,
        limit=limit,
        total_items=total_items,
        total_pages=total_pages,
    )
