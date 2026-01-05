from fastapi import APIRouter
from db.store import seats
router = APIRouter()

@router.get("/")
def get_seats():
    return {"seatData": seats}