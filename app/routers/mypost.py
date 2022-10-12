from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from typing import List, Optional 
from sqlalchemy import func
from .. import mymodels, myschemas, oauth2
from ..dbase import get_db 

router = APIRouter(
    prefix = '/posts',
    tags = ['posts']
)


@router.get("/", response_model = List[myschemas.P_Response])
def get_posts(db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    
    posts = db.query(mymodels.Post, func.count(mymodels.Like.post_id).label("likes")).join(
        mymodels.Like, mymodels.Like.post_id == mymodels.Post.id, isouter = True).group_by(mymodels.Post.id).filter(
            mymodels.Post.title.contains(search)).limit(limit).offset(skip).all()
        
    return posts 


@router.post('/', status_code = status.HTTP_201_CREATED, response_model = myschemas.Post)
def create_post(post : myschemas.P_Create,  db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user )):
    
    new_post = mymodels.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get('/{id}', response_model = myschemas.P_Response)
def get_1_post(id: int, db:Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):
    
    posts = db.query(mymodels.Post, func.count(mymodels.Like.post_id).label("likes")).join(
        mymodels.Like, mymodels.Like.post_id == mymodels.Post.id, isouter = True).group_by(mymodels.Post.id).filter(mymodels.Post.id == id).first()
    
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    
    return posts
    
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)    
def delete_post(id:int, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(mymodels.Post).filter(mymodels.Post.id == id)
    post = post_query.first()
    
    if post == None:
        
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} does not exist")
    
    if post.owner_id != current_user.id:
        
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not authorized to perform this requested action!")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}",status_code = status.HTTP_404_NOT_FOUND, response_model = myschemas.Post)
def update_post(id:int , updated_post : myschemas.P_Create, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(mymodels.Post).filter(mymodels.Post.id == id)
    post = post_query.first()
    
    if post == None:
        
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id :{id} does not exist")
    
    if post.owner_id != current_user.id:
        
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You are not authorized to perform this requested action!")
    
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit() 
    
    return post_query.first()