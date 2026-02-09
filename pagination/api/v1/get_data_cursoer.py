from fastapi import APIRouter, Query
from store.db import store_data
from models.models import CursorPaginatedResponse,Status,Order,SortBy
from services.helper import apply_filter
router = APIRouter()
import math
@router.get("/")
def get_cursor_items(
    limit: int = Query(10, ge=1, le=50),
    cursor: str | None = None
):
    if not cursor:
        return CursorPaginatedResponse(
            
        )