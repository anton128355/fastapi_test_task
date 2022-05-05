from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):

    username: Optional[str] = "random_str"
    email: Optional[EmailStr] = "random_str@gmail.com"
    password: Optional[str] = "random_str"


class UserDB(UserSchema):
    id: int
