from exceptions.exceptions import OTPRecentlySent, MaxOTPRequestsReached, UserDoesNotExist, OTPExpired, UserAlreadyAuthenticated, OTPNotRequested
from db.data import users,otp_store
from db.update_data import Add_Otp,Add_User
from datetime import datetime, timedelta
from service.smtp_send_otp import send_otp
from random import randint

def generate_otp() -> str:
    return str(randint(100000, 999999))

def validate_user_can_request_otp(email: str, now: datetime) -> None:
    user = users[email]

    if user["is_authenticated"]:
        raise UserAlreadyAuthenticated()

    if user["last_otp_request_at"] is None:
        return

    seconds_since_last_request = (
        now - user["last_otp_request_at"]
    ).total_seconds()

    if seconds_since_last_request < 300:
        raise OTPRecentlySent()

    if user["otp_requests"] >= 3 and seconds_since_last_request < 3600:
        raise MaxOTPRequestsReached()




def create_user(email):
    Add_User(email=email, is_authenticated=False,
                 last_requested_otp=None,otp_requests=0) #last_requested_otp should be null or something when creating user i guess

def record_otp_request(email, otp):
    now = datetime.now()

    Add_Otp(
        email=email,
        otp=otp,
        created_at=now,
        expires_at=now + timedelta(minutes=5),
        is_used=False,
    )

    users[email]["last_otp_request_at"] = now
    users[email]["otp_requests"] += 1


def reset_otp_request_counter(email):
    users[email]["otp_requests"] = 0




def send_otp_service(email: str) -> None:
    now = datetime.now()

    if email not in users:
        create_user(email)

    validate_user_can_request_otp(email, now)

    user = users[email]

    if (
        user["last_otp_request_at"] is not None
        and (now - user["last_otp_request_at"]).total_seconds() >= 3600
    ):
        reset_otp_request_counter(email)

    otp = generate_otp()
    record_otp_request(email=email, otp=otp)

    send_otp(email=email, otp=otp)

    