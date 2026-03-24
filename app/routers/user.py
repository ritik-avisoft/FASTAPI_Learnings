from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..utils.hash_password import Hash


router=APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id: {id} does not exist")
    return user

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