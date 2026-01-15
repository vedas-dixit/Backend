from models.models import IdempotencyData
from typing import Dict

idempotency_store: Dict[str, IdempotencyData] = {} #store the key -> data