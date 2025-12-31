class OTPRecentlySent(Exception):
    pass

class MaxOTPRequestsReached(Exception):
    pass

class OTPExpired(Exception):
    pass

class UserDoesNotExist(Exception):
    pass

class InvalidOTP(Exception):
    pass

class UserAlreadyAuthenticated(Exception):
    pass

class OTPNotRequested(Exception):
    pass