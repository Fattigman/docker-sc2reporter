
from typing import  Optional
from fastapi import APIRouter, Depends, Query, Header, Body
from fastapi.security import OAuth2PasswordRequestForm

from authentication import *
from crud.users import get_user, create_user, get_users, del_user

from models import User, Basic_User

router = APIRouter()

@router.get("/", response_model=list[Basic_User])
async def read_users_me(
        current_user: User = Depends(get_current_active_user)
    ):
    if current_user['scope'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admins can see other users",
            headers={"WWW-Authenticate": "Bearer"},
        )
    users = await get_users()
    return [{key:user[key] for key in user if key != 'password'} for user in users]

@router.get("/me/", response_model=Basic_User)
async def read_users_me(
        current_user: User = Depends(get_current_active_user)
    ):
    return {key:current_user[key] for key in current_user if key != 'password'}


@router.get("/me/items/")
async def read_own_items(
        current_user: User = Depends(get_current_active_user)
    ):
    return [{"item_id": "Foo", "owner": current_user['username']}]

@router.post("/add/", response_model=User, status_code=201)
async def post_user(
        user: User,
        current_user: User = Depends(get_current_active_user)
    ):
    if current_user['scope'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admins can create other users",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif await get_user(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists in the database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    create_user(user)
    return user

@router.delete("/delete/", response_model=str)
async def delete_user(
    user: str,
    current_user: User = Depends(get_current_active_user)
    ):
    if user == 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can't delete the admin user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    deleted_user = await del_user(user)
    return f'{user} deleted'