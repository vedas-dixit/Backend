from fastapi import APIRouter,HTTPException,status
from services.reserve_seat import reserve_seat
from utils.exceptions import SeatDoesNotExist,ActiveReservationForThisSeat,SeatUnavailable,UserAlreadyHasActiveReservation,UserDoesNotExist
from models.model import ReserveSeatRequest
router = APIRouter()

@router.post("/")
def reserve_seat_func(request: ReserveSeatRequest):
    try:
        reserved_seat_data = reserve_seat(request.user_email,request.seat_id)
        return{"response":reserved_seat_data}
    except SeatDoesNotExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Seat Number"
        )
    except SeatUnavailable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat is already booked"
        )
    except UserDoesNotExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
    except UserAlreadyHasActiveReservation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active reservation"
        )
    except ActiveReservationForThisSeat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="This seat is already reserved"
        )
    