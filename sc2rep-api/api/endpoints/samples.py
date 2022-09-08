from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from db import *
from models import *
from authentication import *

router = APIRouter()


@router.get("/")
async def read_samples(
    current_user: User = Depends(get_current_active_user)
    ):
    samples = await get_samples()

    return samples

@router.get("/single/{sample_id}")
async def single_sample(
    sample_id: str,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_single_sample(sample_id)

@router.get("/multiple/")
async def multiple_samples(
    sample_ids:list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_multiple_samples(sample_ids)