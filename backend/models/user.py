from pydantic import BaseModel
from typing import Union, Literal

"""
Here we define the models for the users.
In order not to leak the password to the frontend,
we have two models, one for the user and one for the admin.
"""


class Basic_User(BaseModel):
    username: str
    email: str
    fullname: str
    disabled: bool = False
    scope: Literal["user", "admin"]


class User(Basic_User):
    password: str
