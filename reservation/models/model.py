from pydantic import BaseModel

class ReserveSeatRequest(BaseModel):
    user_email: str
    seat_id: str

class BookSeatRequest(BaseModel):
    user_email: str
    seat_id: str