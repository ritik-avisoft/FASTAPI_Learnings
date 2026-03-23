from pwdlib import PasswordHash

pwd_context= PasswordHash.recommended()

def Hash(password:str):
    return pwd_context.hash(password)