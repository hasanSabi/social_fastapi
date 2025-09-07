from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, auth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/comment",
    tags=["Comments"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
   
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {comment.post_id} not found")

    new_comment = models.Comment(**comment.dict(), user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{post_id}", response_model=List[schemas.CommentOut])
def get_comments_for_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No comments found for post with id: {post_id}")
    return comments