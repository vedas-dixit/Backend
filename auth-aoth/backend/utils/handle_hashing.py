import bcrypt

def hash_pass(pasword: str):
    pass_in_bytes = pasword.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(pass_in_bytes,salt)
    return hashed_pass

def check_pass(password: str, hashed_pass: str):
    pass_in_bytes = password.encode('utf-8')
    hashed_bytes = hashed_pass.encode('utf-8')
    return bcrypt.checkpw(pass_in_bytes,hashed_bytes)