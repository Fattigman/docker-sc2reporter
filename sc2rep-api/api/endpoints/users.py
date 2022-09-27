
from typing import  Optional
from fastapi import APIRouter, Depends, Query, Header, Body
from fastapi.security import OAuth2PasswordRequestForm

from db import *
from authentication import *
from crud.users import *

from models import User

router = APIRouter()

@router.get("/me/", response_model=User)
async def read_users_me(
        current_user: User = Depends(get_current_active_user)
    ):
    return current_user


@router.get("/me/items/")
async def read_own_items(
        current_user: User = Depends(get_current_active_user)
    ):
    return [{"item_id": "Foo", "owner": current_user['username']}]

@router.post("/add/", response_model=User)
async def post_user(
        user: User,
        current_user: User = Depends(get_current_active_user)
    ):
    if get_user(user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists in the database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    create_user(user)
    return user

