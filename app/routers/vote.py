from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, auth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if not found_vote:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"message": "Vote added successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vote already exists")
    else:
        if found_vote:
            db.delete(found_vote)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")

