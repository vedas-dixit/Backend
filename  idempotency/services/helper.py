from store.db import idempotency_store
from models.models import IdempotencyStatus
import time

def validate_key_exist(Idempotency_key: str) -> bool:
    return (Idempotency_key in idempotency_store)


def process_data(idempotency_key: str):
    idempotency_store[idempotency_key].status = IdempotencyStatus.in_progress
    time.sleep(4)
    idempotency_store[idempotency_key].status = IdempotencyStatus.completed
    pass

# def process_new_idempotency_data(NewIdempotencyData: IdempotencyData):
#     try:
#         idempotency_store[NewIdempotencyData.idempotency_key] = NewIdempotencyData
#         process_data(NewIdempotencyData.idempotency_key)
#     except Exception as e:
#         print("something went wrong:",e)

# def get_idempotency_data(NewIdempotencyData: IdempotencyData) -> IdempotencyResponse:
#     if validate_key_exist(NewIdempotencyData.idempotency_key):
#         return IdempotencyResponse(
#             idempotency_key=NewIdempotencyData.idempotency_key,
#             status=NewIdempotencyData.status
#         )
#     process_new_idempotency_data(NewIdempotencyData)
#     return IdempotencyResponse(
#         idempotency_key=NewIdempotencyData.idempotency_key,
#         status=NewIdempotencyData.status
#     )
