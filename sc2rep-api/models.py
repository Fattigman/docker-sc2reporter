from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

from typing import Union

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    fullname: Union[str, None] = None
    disabled: Union[bool, None] = None
    password: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(User):
    hashed_password: str