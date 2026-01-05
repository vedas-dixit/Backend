from db.store import seats,users,reservations
from services.create_data import create_user,create_reservations
from datetime import datetime
from db.dataModel import Reservation
from uuid import uuid4
from utils.helper_func import get_or_create_user,validate_seat_exists_and_not_booked,validate_seat_not_reserved,validate_user_has_no_active_reservation


def reserve_seat(user_email: str, seat_id:str) -> Reservation:
    now = datetime.now()
    user = get_or_create_user(user_email=user_email)
    validate_seat_exists_and_not_booked(seat_id=seat_id)
    validate_seat_not_reserved(seat_id=seat_id,now=now)
    validate_user_has_no_active_reservation(now=now,user_id=user.user_id)
    return create_reservations(user_id=user.user_id,seat_id=seat_id,curr_time=now)
    