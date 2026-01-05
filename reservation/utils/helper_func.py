from db.store import users,seats,reservations
from services.create_data import create_user
from db.dataModel import Users,Reservation, Seat
from utils.exceptions import UserDoesnotBelobgToThisReservation, NoActiveReservationForThisSeat, SeatDoesNotExist, UserDoesNotExist, SeatUnavailable,ActiveReservationForThisSeat, ActiveReservationExistForThisUser

def get_or_create_user(user_email: str) -> Users:
    for user in users.values():
        if user.email == user_email:
            return user
    return create_user(email=user_email);

def get_reservation_data(user_id,now) -> Reservation | None:
    for reservation in reservations.values():
        if reservation.user_id == user_id and reservation.expires_at>now and reservation.confirmed_at is None:
            return reservation
    return None

def validate_seat_exists_and_not_booked(seat_id):
    if seat_id not in seats:
        raise SeatDoesNotExist()
    if seats[seat_id].booked_at is not None:
        raise SeatUnavailable()
    return
            

def validate_user_has_no_active_reservation(user_id,now):
    reservation = get_reservation_data(user_id, now)
    if reservation is not None:
        raise ActiveReservationExistForThisUser()
    
def validate_seat_not_reserved(seat_id, now):
    for reservation in reservations.values():
        if reservation.seat_id == seat_id and reservation.confirmed_at is None and reservation.expires_at > now:
            raise ActiveReservationForThisSeat()


#NOTE: BOOKING LOGIC



def validate_user_exist(user_email: str) -> str:
    for user in users.values():
        if user.email == user_email:
            return user.user_id
    raise UserDoesNotExist()
    
def get_active_reservation_for_seat(seat_id: str,now)-> Reservation:
    for reservation in reservations.values():
        if reservation.seat_id == seat_id and reservation.expires_at > now and reservation.confirmed_at is None:
            return reservation
    raise NoActiveReservationForThisSeat()

def validate_user_belongs_to_this_reservation(user_id,reservation_id):
    if user_id != reservations[reservation_id].user_id:
        raise UserDoesnotBelobgToThisReservation()
    

def confirm_booking(seat_id: str,reservation_id,now)-> Seat:
    reservations[reservation_id].confirmed_at = now
    seats[seat_id].booked_at = now
    return Seat(seat_id = seat_id, booked_at= now)

    