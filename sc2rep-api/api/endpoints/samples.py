from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from crud.samples import *
from models import *
from authentication import *

from pprint import pprint
router = APIRouter()


@router.get("/", response_model=list[Sample])
async def read_samples(
    # current_user: User = Depends(get_current_active_user)
    ):
    # samples = await get_samples()
    samples = await test()
    return samples

@router.get("/{sample_id}", response_model=list[Sample])
async def single_sample(
    sample_id: str,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_single_sample(sample_id)

@router.get("/multiple/", response_model=list[Sample])
async def multiple_samples(
    sample_ids:list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_multiple_samples(sample_ids)

@router.get("/pango/", response_model=list[Sample])
async def get_samples_with_pangotype(
    pangolin:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_pangotype_samples(pangolin=pangolin)

@router.get("/variant/", response_model=list[Sample])
async def get_samples_with_variant(
    variant:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_variant_samples(variant=variant)

@router.get("/nextclade/", response_model=list[Sample])
async def get_samples_with_nextclade(
    nextclade:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_nextclade_samples(nextclade=nextclade)