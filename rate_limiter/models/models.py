from pydantic import BaseModel

from datetime import datetime
class ApiRequest(BaseModel):
    user_id: str
    ip_address: str


class UserData(BaseModel):
    user_id: str
    ip_address: str
    window_start: datetime
    count: int

class RequesrResponse(BaseModel):
    allowed: str
    remaining: int
    reset_at: datetime
