from re import M
from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

import pandas as pd 

from crud.samples import *
from crud.matrix import * 
from models import *
from authentication import *

from pprint import pprint
router = APIRouter()

# Gets all samples 
@router.get("/", response_model=list[Sample])
async def read_samples(
    current_user: User = Depends(get_current_active_user)
    ):
    samples = await get_samples()
    return samples

# Gets single specific sample
@router.get("/{sample_id}", response_model=list[Sample])
async def single_sample(
    sample_id: str,
    current_user: User = Depends(get_current_active_user)
    ):
    sample_info = await get_single_sample(sample_id)
    if len(sample_info) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sample can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    matrix = await get_matrix()
    del matrix[0]['_id']
    df = pd.DataFrame(matrix[0])
    distances = abs(df.subtract(df[sample_id], axis = 0)).sum()
    similar_samples = distances[abs(distances) < 10].index.tolist()
    sample_info[0]['similar_samples'] = similar_samples

    return sample_info

# Gets multiple specified samples
@router.get("/multiple/", response_model=list[Sample])
async def multiple_samples(
    sample_ids:list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_multiple_samples(sample_ids)

# Gets all samples with matching specified pango type
@router.get("/pango/", response_model=list[Sample])
async def get_samples_with_pangotype(
    pangolin:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_pangotype_samples(pangolin=pangolin)

# Gets all samples with matching specified variant
@router.get("/variant/", response_model=list[Sample])
async def get_samples_with_variant(
    variant:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_variant_samples(variant=variant)

# Gets all samples with matching specified nextclade
@router.get("/nextclade/", response_model=list[Sample])
async def get_samples_with_nextclade(
    nextclade:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    return await get_nextclade_samples(nextclade=nextclade)
