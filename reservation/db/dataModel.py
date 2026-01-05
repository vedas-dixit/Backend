from dataclasses import dataclass
from datetime import datetime
from typing import Optional
@dataclass
class Users:
    user_id: str
    email: str

@dataclass
class Seat:
    seat_id: str
    booked_at: Optional[datetime] = None

@dataclass
class Reservation:
    reservation_id: str
    user_id: str
    seat_id: str
    created_at: datetime
    expires_at: datetime
    confirmed_at: Optional[datetime] = None


    