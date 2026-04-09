# in-memory "DB"
fake_users_db = {}
fake_token_db = {}
from models.user import UserInDB
def add_user(username, password):
    new_user = UserInDB(password=password,user_name=username)
    fake_users_db[new_user.user_id] = new_user
    return new_user

def store_user_token(user_id, access_token,refresh_token):
    fake_token_db[user_id] = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
