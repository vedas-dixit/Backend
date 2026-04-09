from datetime import datetime, timedelta, timezone
import jwt
from models.user import User
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN_SECREAT = os.getenv("ACCESS_SECRET")
REFRESH_TOKEN_SECREAT = os.getenv("REFRESH_SECRET")

def generate_access_token(user_id):
    payload = {
        "sub":user_id,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=15),
    }
    return jwt.encode(payload=payload,key=ACCESS_TOKEN_SECREAT, algorithm="HS256")

def generate_refresh_token(user_id):
    payload = {
        "sub":user_id,
        "exp":datetime.now(timezone.utc)+timedelta(days=7),
    }
    return jwt.encode(payload=payload,key=REFRESH_TOKEN_SECREAT, algorithm="HS256")

def validate_access_token(user:User) -> bool:
    pass
