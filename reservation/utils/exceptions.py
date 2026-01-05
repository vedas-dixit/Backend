class UserDoesNotExist(Exception):
    pass

class SeatDoesNotExist(Exception):
    pass

class SeatUnavailable(Exception):
    pass

class ReservationExpired(Exception):
    pass

class ActiveReservationExistForThisUser(Exception):
    pass

class ActiveReservationForThisSeat(Exception):
    pass

class UserAlreadyHasActiveReservation(Exception):
    pass

class NoActiveReservationForThisSeat(Exception):
    pass

class UserDoesnotBelobgToThisReservation(Exception):
    pass
