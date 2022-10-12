from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import mymodels, myschemas, hash_pwd
from ..dbase import get_db


router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = myschemas.U_Response)
def create_user(user : myschemas.UserCreate, db : Session = Depends(get_db)):
    
    hash_password = hash_pwd.hash(user.password)
    user.password = hash_password 
    new = mymodels.User(**user.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new 

@router.get('/{id}', response_model = myschemas.U_Response)
def get_user(id : int , db : Session = Depends(get_db)):
    
    user = db.query(mymodels.User).filter(mymodels.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id : {id} does not exist")
    
    return user 