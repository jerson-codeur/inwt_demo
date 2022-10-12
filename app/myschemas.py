from pydantic import BaseModel, EmailStr
from datetime import datetime 
from typing import Optional
from pydantic.types import conint 

class PostMain(BaseModel):
    
    title : str 
    content : str 
    published : bool  

class P_Create(PostMain):
    pass

class U_Response(BaseModel):
    id : int 
    email : EmailStr 
    created_at : datetime
    
    class Config :
        orm_mode = True

     
class Post(PostMain):
    id : int
    created_at : datetime
    owner_id : int
    owner : U_Response
        
        
    class Config :
        orm_mode = True

class P_Response(BaseModel):
    
    Post : Post 
    likes : int
    
class UserCreate(BaseModel):
    
    email : EmailStr 
    
    password : str 
        
        
class UserLogin(BaseModel):
    
    email : EmailStr 
    password : str
    
class Token(BaseModel):
    
    access_token : str 
    token_type : str
    
class TokenData(BaseModel):
    
    id : Optional[str] = None
     
class Like(BaseModel):
    post_id : int 
    dir : conint(le = 1)