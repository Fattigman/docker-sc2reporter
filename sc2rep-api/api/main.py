from db import * 

from authentication import *
from models import *

from api.endpoints import samples, users, login

from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import os

if os.getenv('MONGO_HOST') != "mongodb": os.environ['MONGO_HOST'] = "localhost"

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
    prefix="/samples",
    tags=["Samples"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    login.router,
    prefix="/login",
    tags=["Login"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

@app.get("/depth")
async def depth(current_user: User = Depends(get_current_active_user)):
    return await get_depth()

@app.get("/variants")
async def variants(current_user: User = Depends(get_current_active_user)):
    return await get_variants()

@app.get("/consensus")
async def consensus(current_user: User = Depends(get_current_active_user)):
    return await get_consensus()
