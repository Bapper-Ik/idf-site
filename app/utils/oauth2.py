from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRATION_TIME = setting.access_token_expiration_time


def create_access_token(data: dict):
    
    try:
        
        data_to_encode = data.copy()
        expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)
        data_to_encode.update({'exp': expires})
        
        encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt

    except JWTError as e:
        raise e



def decode_token(token: str, credential_exception):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise credential_exception


def verify_access_token(token: str, credential_exception):
    payload = decode_token(token, credential_exception)
    user_object = payload.get('user_info')
    id: int = user_object['id']
    username: str = user_object['username']
    role: int = user_object['role']
    
    if (username is None) or (role is None):
        raise credential_exception
    
    return {"id": id, "username": username, "role": role}



def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exceptions)
