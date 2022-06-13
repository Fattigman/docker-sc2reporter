from db import * 

from authentication import *
from models import *

from api.endpoints import samples, users

from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title='SarsCov 2 API', 
    description='API for SarsCov 2 visualisation tool', 
    version='development')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {'message': 'Hello and welcome to the SarsCov 2 API'}

app.include_router(
    samples.router,
    prefix="/sample",
    tags=["Samples"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

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

@app.get("/depth")
async def depth(current_user: User = Depends(get_current_active_user)):
    return await get_depth()

@app.get("/variants")
async def variants(current_user: User = Depends(get_current_active_user)):
    return await get_variants()

@app.get("/consensus")
async def consensus(current_user: User = Depends(get_current_active_user)):
    return await get_consensus()
