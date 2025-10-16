from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    profile_image: Optional[str]
    date_of_birth: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    profile_image: Optional[str]

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordChnage(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str