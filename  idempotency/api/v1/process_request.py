from fastapi import APIRouter, BackgroundTasks
from models.models import IdempotencyRequest, IdempotencyData,IdempotencyStatus
from services.helper import process_data
from store.db import idempotency_store
from datetime import datetime, timedelta
router = APIRouter()

@router.post("/")
def process_request(request: IdempotencyRequest, background_tasks: BackgroundTasks):
    try:
        key = request.idempotency_key
        now = datetime.now()
        if key in idempotency_store:
            if now <= idempotency_store[key].created_at + timedelta(seconds=30):
                return {
                    "status": idempotency_store[key].status,
                    "data": idempotency_store[key]
                }
            return {
                "status": "expired",
                "data": idempotency_store[key]
            }
        idempotency_store[key] = IdempotencyData(
            idempotency_key=key,
            payload=request.payload,
            status=IdempotencyStatus.pending,
            created_at=datetime.now()
        )
        background_tasks.add_task(process_data, key)
        return {
                "status":"ok",
                "data": idempotency_store[key]
            }
    except Exception as e:
        print(e)
        return {
            "status": "error",
            "message": str(e)
        }