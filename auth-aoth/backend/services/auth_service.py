from db.users import add_user, fake_users_db,store_user_token
from models.user import User
from utils.handle_token_generate import generate_access_token,generate_refresh_token
from utils.handle_hashing import hash_pass,check_pass

def find_by_username(username):
    for user in fake_users_db.values():
        if user.user_name == username:
            return user
    return None

def HandelSignup(user: User):
    if find_by_username(user.user_name):
        return {"err":"user exist"}
    hashed_pass = hash_pass(user.password)
    new_user = add_user(username=user.user_name, password=hashed_pass)

    access = generate_access_token(user_id=new_user.user_id)
    refresh = generate_refresh_token(user_id=new_user.user_id)
    store_user_token(access_token=access,refresh_token=refresh,user_id=new_user.user_id)

    return {"success":"user created sucessfully", "access-token":access,"refresh-token":refresh}
    

def handelLogin(user: User):
    user_data = find_by_username(username=user.user_name)
    if not user_data:
        return {"err":"user doesn't exist"}
    
    if not check_pass(hashed_pass=user_data.password, password=user.password):
        return {"err":"invalid pss"}
    return {"message": "login sucessful"}
    
