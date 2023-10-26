from pydantic import BaseModel
from typing import Union
from .user import User

"""
Here we define the models for the login.
Tokens are used to authenticate the user.
They are jwt tokens, which are signed with a secret key.
"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(User):
    hashed_password: str
