from services.helper import get_idempotency_data
from models.models import IdempotencyRequest,IdempotencyData,IdempotencyStatus

def helper_process_request(request: IdempotencyRequest) -> IdempotencyRequest:
    try:
        NewIdempotencyData = IdempotencyData(
            idempotency_key= request.idempotency_key,
            payload=request.payload,
            status= IdempotencyStatus.pending
        )
        idempotency_process_response = get_idempotency_data(NewIdempotencyData)
        return idempotency_process_response
    except Exception as e:
        raise ("someting went wrong",e)

# Rules
# If idempotency_key is new:
# Process the request
# Store the result
# Return success

# If idempotency_key is already processed:
# Do NOT process again
# Return the same response as before