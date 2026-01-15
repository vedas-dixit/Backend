from db.data import users
from datetime import datetime
from services.helper_func import validate_user_exist, validate_user_request_limit
def check_rate_limit(user_id,ip_address):
    now = datetime.now()
    user = validate_user_exist(user_id=user_id,ip_address=ip_address,now=now)
    validate_user_request_limit(user_id=user_id,now=now)
    #validate if user exist
        #NO-> create user
    #validate if user is allowed to get respose
        #check if user requested more then 5 request in last minute
        #check if user 
    #update user request counter | last requested | give respoine