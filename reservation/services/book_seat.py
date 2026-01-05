from utils.helper_func import validate_user_belongs_to_this_reservation,get_active_reservation_for_seat,validate_user_exist,validate_seat_exists_and_not_booked, confirm_booking
from datetime import datetime
from db.dataModel import Seat

def book_seat_flow(user_email, seat_id) -> Seat: 
    now = datetime.now()
    # 1. Resolve user (must exist)
    user_id = validate_user_exist(user_email=user_email)
    # 2. Validate seat exists & Validate seat is not already booked
    validate_seat_exists_and_not_booked(seat_id=seat_id)
    # 4. Find active reservation for this seat | If no active reservation → reject
    reservation = get_active_reservation_for_seat(seat_id= seat_id, now=now)
    # 6. If reservation.user_id != this user → reject
    validate_user_belongs_to_this_reservation(reservation_id=reservation.reservation_id,user_id=user_id)
    # 7. Confirm booking:
    #    - reservation.confirmed_at = now
    #    - seat.booked_at = now
    return confirm_booking(now=now,reservation_id=reservation.reservation_id,seat_id=seat_id)


    


