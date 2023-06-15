from typing import Optional, Union
from fastapi import Depends, HTTPException, Query
from fastapi import APIRouter


import pandas as pd 

from crud import samples, get_matrix, variants

from models import *
from authentication import *

router = APIRouter()

import time

# Gets all samples 
@router.get("/", response_model = list[Sample])
async def read_samples(
    current_user: User = Depends(get_current_active_user),
    advanced_search: Optional[bool] = False,
    ): 

    sample_list = await samples.get_samples(advanced_search)
    return sample_list

# Gets single specific sample
@router.get("/{sample_id}")
async def single_sample(
    sample_id: str,
    current_user: User = Depends(get_current_active_user)
    ):
    sample_info = await samples.get_single(sample_id, id_field='sample_id')
    if len(sample_info) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sample can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    matrix = await get_matrix()
    del matrix[0]['_id']
    df = pd.DataFrame(matrix[0])
    if sample_id in df.columns:
        distances = abs(df.subtract(df[sample_id], axis = 0)).sum()
        similar_samples = distances[abs(distances) < 10].index.tolist()
    variant_info = await variants.get_multiple([x['id'] for x in sample_info[0]['variants']])
    return {"sampleInfo":sample_info, "similarSamples": similar_samples, "variantInfo": variant_info}


# Delete multiple samples and all associated data
@router.delete("/", response_model=list[Sample])
async def delete_samples(
    sample_id: list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user)
    ):
    if current_user['scope'] == 'user':
        raise HTTPException(status_code=403, detail="Not allowed")
    samples_to_delete = await samples.get_multiple(sample_id, id_field='sample_id')
    await samples.delete_samples(sample_id)
    return samples_to_delete

# Gets multiple specified samples
@router.get("/multiple/", response_model=list[Sample])
async def multiple_samples(
    sample_id:list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user)
    ):
    return await samples.get_multiple(sample_id, id_field='sample_id')

# Gets all samples with matching specified pango type
@router.get("/pango/", response_model=GroupedSamples)
async def get_samples_with_pangotype(
    pangolin:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    samples_list = await samples.get_pangotype_samples(pangolin)
    samples_list = [sample for sample in samples_list if 'collection_date' in sample]
    graph_list = group_by_dict(samples_list)
    return {'samples': samples_list, 'graph': graph_list}

# Gets all samples with matching specified variant
@router.get("/variant/", response_model=GroupedVariantSamples)
async def get_samples_with_variant(
    variant:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    samples_list = await samples.get_variant_samples(variant=variant)
    samples_list = [sample for sample in samples_list if 'collection_date' in sample]
    variant_info = await variants.get_single(variant)
    graph_list = group_by_dict(samples_list)
    return {'samples': samples_list, 'graph': graph_list, 'variantInfo': variant_info}

# Gets all samples with matching specified nextclade
@router.get("/nextclade/", response_model=GroupedSamples)
async def get_samples_with_nextclade(
    nextclade:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    samples_list = await samples.get_nextclade_samples(nextclade=nextclade)
    samples_list = [sample for sample in samples_list if 'collection_date' in sample]
    graph_list = group_by_dict(samples_list)
    return {'samples': samples_list, 'graph': graph_list}

def group_by_dict(samples:dict):
    # group by key
    graph_list = {}
    for sample in samples:
        # sample_time = (time.strftime('%Y-%m-%w', time.localtime(sample['collection_date']['$date']/1000))) # convert epoch to datetime
        sample_time = datetime.fromtimestamp(sample['collection_date']['$date']/1000)
        sample_time = sample_time.strftime('%Y-%m')+f'-{sample_time.day//7+1}'

        if sample_time in graph_list:
            graph_list[sample_time] += 1
        else:
            graph_list[sample_time] = 1
    # sort by key
    graph_list = {k: v for k, v in sorted(graph_list.items(), key=lambda item: item[0])}
    graph_list = [{'date': k, 'count': v} for k, v in graph_list.items()]
    return graph_list
