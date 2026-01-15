from db.data import users
from models.models import UserData
from datetime import datetime
LIMIT = 5
WINDOW_SECONDS = 60
def create_user(user_id,ip_address,now):

    users[user_id] = UserData(
        user_id=user_id,
        ip_address=ip_address,
        count = 0,
        window_start = now
    )
    return users[user_id]


def validate_user_exist(user_id:str,ip_address:str,now:datetime)-> UserData:
    if user_id not in users:
        return create_user(user_id,ip_address,now)
    return users[user_id]

def validate_user_request_limit(user_id:str,now:datetime):
    user = users[user_id]
    if (now - user.window_start).total_seconds() >= WINDOW_SECONDS:
        user.window_start = now
        user.count = 0

    if user.count >= LIMIT:
        raise Exception("Request limit exceeded, wait for",WINDOW_SECONDS - int(user.window_start.total_seconds()))

    user.count += 1
    return user
    