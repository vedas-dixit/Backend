from typing import List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class DataModel(BaseModel):
    id: int
    amount: float
    status: Status
    created_at: datetime

class SortBy(str, Enum):
    created_at = "created_at"
    amount = "amount"

class Order(str, Enum):
    asc = "asc"
    desc = "desc"

class PaginatedResponse(BaseModel):
    page: int
    limit: int
    total_items: int
    total_pages: int
    data: List

class CursorPaginatedResponse(BaseModel):
    limit: int
    total_items: int
    data: List
