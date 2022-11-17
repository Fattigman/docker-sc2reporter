from db import * 

from authentication import *
from models import *

from api.config import * 

from api.endpoints import samples, users, login, variants, dashboard, phyllogeny

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware



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

app.include_router(
    variants.router,
    prefix="/variants",
    tags=["Variants"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    phyllogeny.router,
    prefix="/phyllogeny",
    tags=["Phyllogeny"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

@app.get("/depth")
async def depth(current_user: User = Depends(get_current_active_user)):
    return await get_depth()


@app.get("/consensus")
async def consensus(current_user: User = Depends(get_current_active_user)):
    return await get_consensus()
