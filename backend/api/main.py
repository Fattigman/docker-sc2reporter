from db import * 

from authentication import *
from models import *

from api.config import settings

from api.endpoints import samples, users, login, variants, dashboard, phyllogeny, consensus, depth, significant_variants

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version='development',
    root_path=settings.ROOT_PATH,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {'message': 'Hello and welcome to the SarsCov 2 API', 'root_path': app.root_path}

app.include_router(
    samples.router,
    prefix="/samples",
    tags=["Samples"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    consensus.router,
    prefix="/consensus",
    tags=["Consensus"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    depth.router,
    prefix="/depth",
    tags=["Depth"],
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
    significant_variants.router,
    prefix="/significant_variants",
    tags=["Significant Variants"],
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

@app.on_event("startup")
async def startup_event():
    await startup_db()