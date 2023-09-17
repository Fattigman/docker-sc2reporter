from fastapi import APIRouter, Depends, Query, Body, HTTPException, status
from crud import depth
from models import Depth, User
from authentication import get_current_active_user
from typing import List

"""
This module contains all the endpoints for the depth collection in the database.
They use the functions from the crud module to interact with the database with the depth model.
"""

router = APIRouter()


@router.get("/", response_model=List[Depth])
async def get_depth_endpoint(current_user: User = Depends(get_current_active_user)):
    """
    Retrieve all depth sequences from the database.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        List[Depth]: A list of depth sequences.
    """
    data = await depth.get()
    return data


@router.get("/{id}", response_model=List[Depth])
async def get_single_depth_endpoint(
    id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a single depth sequence by its ID.

    Args:
        id (str): The ID of the depth sequence to retrieve.
        current_user (User): The current authenticated user.

    Returns:
        List[Depth]: A list containing the retrieved depth sequence.
    """
    data = await depth.get_single(id, "sample_id")

    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="depth sequence can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data


@router.get("/multiple", response_model=List[Depth])
async def get_multiple_depth_endpoint(
    ids: List[str],
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve multiple depth sequences by their IDs.

    Args:
        ids (List[str]): A list of IDs of the depth sequences to retrieve.
        current_user (User): The current authenticated user.

    Returns:
        List[Depth]: A list containing the retrieved depth sequences.
    """
    data = await depth.get_multiple(ids, "sample_id")
    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="depth sequences can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data


@router.put("/{id}")
async def update_depth_endpoint(
    id: str, obj_in: Depth, current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing depth sequence in the database by its ID.

    Args:
        id (str): The ID of the depth sequence to update.
        obj_in (Depth): The updated depth object.
        current_user (User): The current authenticated user.

    Returns:
        dict: A dictionary indicating the update status.
    """
    data = await depth.update(id, obj_in, "sample_id")
    if not data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sample failed to update in the database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {f"{id}": "failed to update"}
