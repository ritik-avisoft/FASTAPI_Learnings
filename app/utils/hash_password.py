from pwdlib import PasswordHash

pwd_context= PasswordHash.recommended()

def Hash(password:str):
    return pwd_context.hash(password)

def Verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)