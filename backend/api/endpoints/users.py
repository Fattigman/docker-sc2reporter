
from typing import  Optional
from fastapi import APIRouter, Depends, Query, Header, Body
from fastapi.security import OAuth2PasswordRequestForm

from authentication import *
from crud.users import get_user, create_user, get_users

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
    if await get_user(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists in the database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    create_user(user)
    return user

