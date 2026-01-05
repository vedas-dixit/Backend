from fastapi import APIRouter,HTTPException,status
from models.model import BookSeatRequest
from services.book_seat import book_seat_flow
from utils.exceptions import UserDoesnotBelobgToThisReservation, NoActiveReservationForThisSeat, SeatDoesNotExist, UserDoesNotExist, SeatUnavailable,ActiveReservationForThisSeat, ActiveReservationExistForThisUser
router = APIRouter()

@router.post("/")
def confirm_seat(request: BookSeatRequest):
    try:
        booked_seat_details = book_seat_flow(seat_id=request.seat_id ,user_email=request.user_email)
        return {"seat booked sucessfully": booked_seat_details}
    except UserDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    except SeatDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat does not exist"
        )

    except NoActiveReservationForThisSeat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active reservation found for this seat"
        )

    except UserDoesnotBelobgToThisReservation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reservation does not belong to this user"
        )

    except SeatUnavailable:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seat is already booked"
        )

    except ActiveReservationExistForThisUser:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has an active reservation"
        )

    