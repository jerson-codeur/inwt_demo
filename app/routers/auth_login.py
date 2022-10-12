from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from .. import dbase, hash_pwd, mymodels, myschemas, oauth2 

router = APIRouter(
    tags = ['Authentification']
)

@router.post('/login', response_model = myschemas.Token)
def login(user : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(dbase.get_db)):
    
    user_tmp = db.query(mymodels.User).filter(mymodels.User.email == user.username).first()
    
    if not user_tmp:
        
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "invalid credentials !")
    
    if not hash_pwd.verify(user.password, user_tmp.password):
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials !")
    
    access_token = oauth2.access_token_data(data = {"user_id":user_tmp.id})
    
    return {"access_token":access_token, "token_type":"bearer"}
