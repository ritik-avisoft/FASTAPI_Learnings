from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.hash_password import Hash

router =APIRouter()


@router.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostBase, db: Session = Depends(get_db)):
    post = models.Post(**new_post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/posts/{id}", response_model=schemas.Post)
def get_single_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()

@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.post("/createusers", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_users(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail=f"user with email: {new_user.email} already exists")
    
    #hashing the pass
    new_user.password = Hash(new_user.password)

    user = models.User(**new_user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
