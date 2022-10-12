from jose import JWTError, jwt 
from datetime import datetime, timedelta
from . import myschemas, dbase, mymodels
from fastapi import  Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth_scheme = OAuth2PasswordBearer(tokenUrl = 'login')
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def access_token_data(data : dict):
    data_encoded = data.copy()
    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    data_encoded.update({"exp":expire})
    jwt_encoded = jwt.encode(data_encoded, SECRET_KEY, ALGORITHM)
    
    return jwt_encoded 

def verify_access_token_data(token : str , credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        id : str = payload.get("user_id")
    
        if id is None:
            raise credentials_exception
    
        token_data = myschemas.TokenData(id = id)
    except JWTError as e: 
        raise credentials_exception
    
    return token_data

def get_current_user(token : str = Depends(oauth_scheme), db : Session = Depends(dbase.get_db)):
    
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                          detail = f"could not validate credential")
    token = verify_access_token_data(token, credentials_exception)
    
    user = db.query(mymodels.User).filter(mymodels.User.id == token.id).first()
    
    return user 
    