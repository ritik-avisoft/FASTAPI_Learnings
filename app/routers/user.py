from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
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

@router.post("/updateprofile")
def update_profile(updated_user: schemas.UserUpdate, db: Session = Depends(get_db), current_user:str = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id: {id} does not exist")
    
    data = updated_user.model_dump(exclude_unset=True)

    if "name" not in data and "phone_number" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of 'name' or 'phone_number' must be provided."
        )

    if "name" in data and (data["name"] is None or data["name"].strip() == ""):
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )

    user_query.update(data, synchronize_session=False)
    db.commit()

    return user_query.first()
