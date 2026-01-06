from pydantic import BaseModel
from datetime import datetime
class ApiRequest(BaseModel):
    user_id: str
    ip_address: str


class UserData(BaseModel):
    user_id: str
    ip_address: str
    total_request: int
    last_requested: datetime

class RequesrResponse:
    allowed: str
    remaining: int
    reset_at: datetime
