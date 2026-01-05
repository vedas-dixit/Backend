from db.dataModel import Users as User,Seat,Reservation

users: dict[str, User] = {}
seats: dict[str, Seat] = {}
reservations: dict[str, Reservation] = {}

seats = {
    "A1": Seat(seat_id="A1"),
    "A2": Seat(seat_id="A2"),
    "A3": Seat(seat_id="A3"),
    "B1": Seat(seat_id="B1"),
}