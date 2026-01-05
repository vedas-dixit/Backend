so we need to make a service that does seat reservation.
now how to reserve a seat is the question?

For someone to reserve a seat:
-> Book a seat by selecting from the available seats & book the one by -> paying for that seat

in order to know about what sets are available
we can make a get -> available seats

we also need to make a post -> book the seat and confirm payment
-> in this there can be some external service for payment 
for simplicity we'll just use a dummy response

there will be a list of seats for sure
each seat will have:

user{
    userid
    booked_Seat: seat_id
}

Seat model
-> seat_number/seat_id : str
-> avability: bool


Seat data
-> seat Id: Str
-> seat expiry: none/datetime
->


endpoints:
GET /seats -> return a list of available seats

Post /reserve -> temperary mark the seat avability as false with a datetime timestamp of expiry of 5 mins

Post /confirm -> thinking about this makes "permananet_book" = true and timestamp dont matter as its checked first


so:
GET /seats: *thinking not sending the seats where avability is already false but this might trigger the one with temperary reservation
returns seats data{
    seat_id = str
}


user{
    user_id
    email
    seat_reserved: none/str
}

seat{
    seat_id
    reserved: bool : temperary reserved
    reserved_expiry: None/datetime: 
    Booked: bool : permanaent booked
}

POST /reserve:



    # NOTE get_or_create_user(email) -> User
    # NOTE validate_seat_exists_and_not_booked(seat_id, now)
    # NOTE validate_user_has_no_active_reservation(user_id, now)
    # NOTE validate_seat_not_reserved(seat_id, now)
    # NOTE create_reservation(user_id, seat_id, now)


users: dict[str, User] = {}
seats: dict[str, Seat] = {}
reservations: dict[str, Reservation] = {}

seats = {
    "A1": Seat(seat_id="A1"),
    "A2": Seat(seat_id="A2"),
    "A3": Seat(seat_id="A3"),
    "B1": Seat(seat_id="B1"),
}

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


    