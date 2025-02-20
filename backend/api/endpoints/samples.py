from typing import Optional, Union
from fastapi import Depends, HTTPException, Query
from fastapi import APIRouter

from api.config import settings
import pandas as pd

from crud import samples, get_matrix, variants, depth

from models import *
from authentication import *

"""
This module contains all the endpoints for the sample collection in the database.
They use the functions from the crud module to interact with the database with the Sample model.
"""

router = APIRouter()


# Gets all samples
@router.get("/", response_model=list[Sample])
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
    current_user: User = Depends(get_current_active_user),
    genetic_distance: Optional[int] = 10,
):
    sample_info = await samples.get_single(sample_id, id_field="sample_id")
    if len(sample_info) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sample can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )

    matrix = await get_matrix()
    dict_to_df = {x["_id"]: x["array"] for x in matrix}
    df = pd.DataFrame(dict_to_df)
    if sample_id in df.columns:
        distances = abs(df.subtract(df[sample_id], axis=0)).sum()
        similar_samples = distances[abs(distances) < genetic_distance].index.tolist()
    similar_samples = [
        {
            "sampleId": x,
            "geneticDistance": distances[x],
        }
        for i, x in enumerate(similar_samples)
    ]
    variant_info = await variants.get_multiple(
        [x["id"] for x in sample_info[0]["variants"]]
    )
    return {
        "sampleInfo": sample_info,
        "similarSamples": similar_samples,
        "variantInfo": variant_info,
    }


# Delete multiple samples and all associated data
@router.delete("/", response_model=list[Sample])
async def delete_samples(
    sample_id: list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user),
):
    if current_user["scope"] == "user":
        raise HTTPException(status_code=403, detail="Not allowed")
    samples_to_delete = await samples.get_multiple(sample_id, id_field="sample_id")
    await samples.delete_samples(sample_id)
    return samples_to_delete


# Gets multiple specified samples
@router.get("/multiple/", response_model=list[Sample])
async def multiple_samples(
    sample_id: list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user),
):
    return await samples.get_multiple(sample_id, id_field="sample_id")


# Gets all samples with matching specified pango type
@router.get("/pango/", response_model=GroupedSamples)
async def get_samples_with_pangotype(
    pangolin: str, current_user: User = Depends(get_current_active_user)
):
    samples_list = await samples.get_pangotype_samples(pangolin)
    samples_list = [sample for sample in samples_list if "collection_date" in sample]
    graph_list = group_by_dict(samples_list)
    return {"samples": samples_list, "graph": graph_list}


# Gets all samples with matching specified variant
@router.get("/variant/", response_model=GroupedVariantSamples)
async def get_samples_with_variant(
    variant_aa: str,
    variant_id: str,
    current_user: User = Depends(get_current_active_user),
):
    samples_list = await samples.get_variant_samples(variant=variant_aa)
    samples_list = [sample for sample in samples_list if "collection_date" in sample]
    variant_info = await variants.get_single(variant_id)
    if variant_aa in settings.COVARIANT_DICT:
        variant_info[0][
            "External link CoVariants"
        ] = f" https://covariants.org/variants/{settings.COVARIANT_DICT[variant_aa]}"
    elif len(variant_info) > 0:
        variant_info[0]["External link CoVariants"] = "Not found"
    else:
        variant_info = [{"Error": f"{variant_id} not found in the database"}]
    graph_list = group_by_dict(samples_list)
    print(variant_info)
    return {"samples": samples_list, "graph": graph_list, "variantInfo": variant_info}


# Gets all samples with matching specified nextclade
@router.get("/nextclade/", response_model=GroupedSamples)
async def get_samples_with_nextclade(
    nextclade: str, current_user: User = Depends(get_current_active_user)
):
    samples_list = await samples.get_nextclade_samples(nextclade=nextclade)
    samples_list = [sample for sample in samples_list if "collection_date" in sample]
    graph_list = group_by_dict(samples_list)
    return {"samples": samples_list, "graph": graph_list}


def group_by_dict(samples: dict):
    # group by key
    graph_list = {}
    for sample in samples:
        # sample_time = (time.strftime('%Y-%m-%w', time.localtime(sample['collection_date']['$date']/1000))) # convert epoch to datetime
        sample_time = datetime.fromtimestamp(sample["collection_date"]["$date"] / 1000)
        sample_time = sample_time.strftime("%Y-%m") + f"-{sample_time.day//7+1}"

        if sample_time in graph_list:
            graph_list[sample_time] += 1
        else:
            graph_list[sample_time] = 1
    # sort by key
    graph_list = {k: v for k, v in sorted(graph_list.items(), key=lambda item: item[0])}
    graph_list = [{"date": k, "count": v} for k, v in graph_list.items()]
    return graph_list
