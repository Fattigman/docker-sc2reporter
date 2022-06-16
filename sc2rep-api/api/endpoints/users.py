
from typing import List, Optional
from fastapi import APIRouter, Depends

from db import *
from authentication import *
from crud.users import create_user

from models import User

router = APIRouter()

@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user['username']}]

@router.post("/add/{user: User}")
async def post_user(user: User = Depends()):
    create_user(user)
    return user