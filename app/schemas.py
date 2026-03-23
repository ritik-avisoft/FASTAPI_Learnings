from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str

class Post(PostBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email: EmailStr
    created_at:datetime
    model_config = {"from_attributes": True}
