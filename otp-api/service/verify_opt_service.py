from datetime import datetime, timedelta
from exceptions.exceptions import UserDoesNotExist,OTPExpired,InvalidOTP,UserAlreadyAuthenticated
from db.data import users, otp_store


def validate_otp(email: str, input_code: str) -> None:
    if email not in otp_store:
        raise OTPExpired()

    otp = otp_store[email]
    now = datetime.now()

    if otp["is_used"]:
        raise OTPExpired()

    if now > otp["expires_at"]:
        raise OTPExpired()

    if otp["code"] != input_code:
        raise InvalidOTP()

def verify_otp_service(email: str, otp: str) -> None:
    if email not in users:
        raise UserDoesNotExist()

    user = users[email]

    if user["is_authenticated"]:
        raise UserAlreadyAuthenticated()

    validate_otp(email, otp)

    otp_store[email]["s_used"] = True
    user["is_authenticated"] = True
    return {"status": "user authenticated"}
