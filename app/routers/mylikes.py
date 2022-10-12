from sys import prefix
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import myschemas, dbase, mymodels, oauth2


router = APIRouter(
    prefix = "/like",
    tags = ['like']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def like(likes : myschemas.Like, db : Session = Depends(dbase.get_db), current_user : int = Depends(oauth2.get_current_user)):
    
    like_query = db.query(mymodels.Like).filter(mymodels.Like.post_id == likes.post_id, mymodels.Like.user_id == current_user.id)
    found_like = like_query.first()
    
    if (likes.dir == 1):
        
        if found_like:
            
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already liked on post {likes.post_id}")
        
        new_like = mymodels.Like(post_id = likes.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "succesfully added like"}
    
    else:
        
        if not found_like:
            
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "does not exist !")
        
        like_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "succesfully deleted !"}