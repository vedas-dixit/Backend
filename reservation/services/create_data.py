from db.store import users,seats,reservations
from random import randint
from datetime import datetime,timedelta
from uuid import uuid4
from db.dataModel import Users as User,Reservation

def create_user(email: str) -> User:
    uid = uuid4()
    user = User(
        user_id=uid,
        email=email
    )
    users[uid] = user
    return user


    
def create_reservations(user_id: str, curr_time: datetime, seat_id: str) -> Reservation:

    rid = uuid4()
    reservation = Reservation (
        reservation_id=rid,
        confirmed_at= None,
        user_id=user_id,
        created_at= curr_time,
        expires_at=curr_time + timedelta(seconds=300),
        seat_id=seat_id
        )

    reservations[rid] = reservation
    return reservations[rid]