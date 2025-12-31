from db.data import users, otp_store, User, Otp
from datetime import datetime

def Add_User(email, is_authenticated, last_requested_otp, otp_requests):
    users[email] = {
        "email": email,
        "is_authenticated": is_authenticated,
        "last_otp_request_at": last_requested_otp,
        "otp_requests": otp_requests
    }

def Add_Otp(email: str, otp: str, created_at, expires_at, is_used: bool):
    otp_store[email] = {
        "email": email,
        "code": otp,
        "created_at": created_at,
        "expires_at": expires_at,
        "is_used": is_used,
    }