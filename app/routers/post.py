from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, auth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

   # posts_with_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    posts_with_counts = (
    db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes"),
        func.count(models.Comment.id).label("comments")
    )
    .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
    .outerjoin(models.Comment, models.Comment.post_id == models.Post.id)
    .group_by(models.Post.id)
    .filter(models.Post.title.contains(search))
    .offset(skip)
    .limit(limit)
    .all()
)

    
    #return [schemas.PostOut(Post=post, votes=votes) for post, votes in results]
    return posts_with_counts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
   # cursor.execute("""INSERT INTO posts (title, content, published) # VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, # post.published))
   # new_post = cursor.fetchone()
   # conn.commit()

   new_post = models.Post(**post.dict(), owner_id=current_user.id)
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post_with_counts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.id).label("comments")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).join(models.Comment, models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post_with_counts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post_with_counts


@router.delete("{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

   # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
   # updated_post = cursor.fetchone()
   # conn.commit()

    post_query =db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
