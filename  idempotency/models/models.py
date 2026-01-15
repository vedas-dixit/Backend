from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class Payload(BaseModel):
    action: str
    amount: int


class IdempotencyRequest(BaseModel):
    idempotency_key: str
    payload: Payload


class IdempotencyStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class IdempotencyResponse(BaseModel):
    idempotency_key: str
    status: IdempotencyStatus

class IdempotencyData(BaseModel):
    idempotency_key: str
    payload: Payload
    status: IdempotencyStatus
    created_at: datetime
    