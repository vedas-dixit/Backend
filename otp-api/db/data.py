from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    email: str
    last_otp_request_at: datetime | None
    otp_requests: int
    is_authenticated: bool


@dataclass
class Otp:
    email: str
    code: str
    created_at: datetime
    expires_at: datetime
    is_used: bool

users: dict[str, User] = {}
otp_store: dict[str, Otp] = {}