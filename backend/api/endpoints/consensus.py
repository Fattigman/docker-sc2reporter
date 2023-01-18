from fastapi import  Depends, Query, Body, HTTPException, status
from crud import consensus
from models import Consensus, User
from authentication import get_current_active_user
from typing import List
from api.router import APIRouter
"""
This module contains all the endpoints for the consensus collection in the database.
They use the functions from the crud module to interact with the database with the Consensus model.
"""
router = APIRouter()

@router.get("/", response_model=List[Consensus])
async def get_consensus_endpoint(
    current_user: User = Depends(get_current_active_user)
):  
    data = await consensus.get()
    return data

@router.get("/{id}", response_model=List[Consensus])
async def get_single_consensus_endpoint(
    id: str = Query(..., description="The sample id of the consensus sequence to get"),
    current_user: User = Depends(get_current_active_user)
):  
    data = await consensus.get_single(id, "sample_id")

    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consensus sequence can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data

@router.get("/multiple", response_model=List[Consensus])
async def get_multiple_consensus_endpoint(
    ids: List[str] = Query(..., description="List of sample ids of the consensus sequences to get"),
    current_user: User = Depends(get_current_active_user)
):  
    data = await consensus.get_multiple(ids, "sample_id")
    if len(data) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consensus sequences can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data

@router.post("/")
async def create_consensus_endpoint(
    obj_in: Consensus = Body(..., description="The consensus object to create"),
    current_user: User = Depends(get_current_active_user)
):
    data = await consensus.create(obj_in)
    if data:
        return {f'{obj_in.sample_id}': 'created successfully'}
    else:
        return {f'{obj_in.sample_id}': 'failed to create'}

@router.put("/{id}")
async def update_consensus_endpoint(
    id: str,
    obj_in: Consensus,
    current_user: User = Depends(get_current_active_user)
):
    data = await consensus.update(id, obj_in, "sample_id")
    if not data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sample failed to update in the database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {f'{id}': 'failed to update'}