from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from db import *
from models import *
from authentication import *

router = APIRouter()


@router.get("/")
async def get_variant_info(
    current_user: User = Depends(get_current_active_user)
    ):
    samples = await get_variants()

    return samples

@router.get("/{variant_id}")
async def single_sample(
    variant_id: str,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_single_variant(variant_id)

@router.post("/multiple/")
async def multiple_samples(
    variant_ids:list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_multiple_variants(variant_ids)

