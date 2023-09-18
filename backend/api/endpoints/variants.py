from fastapi import APIRouter, Depends, Query, Body, HTTPException, status
from ...crud import variants
from ...models import User, Variant
from ...authentication import get_current_active_user
from typing import List


"""
This module contains all the endpoints for the Variant collection in the database.
They use the functions from the crud module to interact with the database with the Variant model.
"""
router = APIRouter()


@router.get("/", response_model=List[Variant])
async def get_Variant_endpoint(current_user: User = Depends(get_current_active_user)):
    data = await variants.get()
    return data


@router.get("/{id}", response_model=List[Variant])
async def get_single_Variant_endpoint(
    id: str,
    current_user: User = Depends(get_current_active_user),
):
    data = await variants.get_single(id)

    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data


@router.get("/multiple", response_model=List[Variant])
async def get_multiple_Variant_endpoint(
    ids: List[str],
    current_user: User = Depends(get_current_active_user),
):
    data = await variants.get_multiple(ids)
    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant sequences can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data


@router.post("/")
async def create_Variant_endpoint(
    obj_in: Variant = Body(..., description="The Variant object to create"),
    current_user: User = Depends(get_current_active_user),
):
    data = await variants.create(obj_in)
    if data:
        return {f"{obj_in.sample_id}": "created successfully"}
    else:
        return {f"{obj_in.sample_id}": "failed to create"}


@router.put("/{id}")
async def update_Variant_endpoint(
    id: str, obj_in: Variant, current_user: User = Depends(get_current_active_user)
):
    data = await variants.update(id, obj_in)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sample failed to update in the database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {f"{id}": "failed to update"}
