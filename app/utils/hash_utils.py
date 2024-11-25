import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, password):
    return bcrypt.chckpw(password.encode('utf-8'), hashed_password)
    