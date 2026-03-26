from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
class UserResponse(BaseModel):
    id:int
    name:str
    email: EmailStr
    created_at:datetime
    model_config = {"from_attributes": True}
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    owner: UserResponse
    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[int] =None

class Vote(BaseModel):
    post_id:int
    dir: Annotated[int, Field(ge=0, le=1)]

class PostOut(BaseModel):
    Post: Post
    votes:int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[int] = None