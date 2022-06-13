from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from db import *
from authentication import *

router = APIRouter()


@router.get("/samples")
async def read_samples(
    current_user: User = Depends(get_current_active_user)
    ):
    samples = await get_all_samples()

    return samples

@router.get("/samples/{sample_id}")
async def sample(
    sample_id: str,current_user: User = Depends(get_current_active_user)
    ):
    return await get_single_sample(sample_id)