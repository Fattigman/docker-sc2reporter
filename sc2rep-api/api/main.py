from db.db import * 

from logic.authentication import *
from models.models import *

from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title='SarsCov 2 API', description='API for SarsCov 2 visualisation tool', version='development')

@app.get('/')
def root():
    return {'message': 'Hello and welcome to the SarsCov 2 API'}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user['username']}]



@app.get("/samples")
async def read_samples(current_user: User = Depends(get_current_active_user)):
    samples = await get_all_samples()

    return samples

@app.get("/samples/{sample_id}")
async def sample(sample_id: str,current_user: User = Depends(get_current_active_user)):
    return await get_single_sample(sample_id)

@app.get("/depth")
async def depth(current_user: User = Depends(get_current_active_user)):
    return await get_depth()

@app.get("/variants")
async def variants(current_user: User = Depends(get_current_active_user)):
    return await get_variants()

@app.get("/consensus")
async def consensus(current_user: User = Depends(get_current_active_user)):
    return await get_consensus()
