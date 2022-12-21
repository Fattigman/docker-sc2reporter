from fastapi import APIRouter, Depends, Query, Body
from crud import consensus
from models import Consensus, User
from authentication import get_current_active_user
from typing import List

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
    return data

@router.get("/multiple", response_model=List[Consensus])
async def get_multiple_consensus_endpoint(
    ids: List[str] = Query(..., description="List of sample ids of the consensus sequences to get"),
    current_user: User = Depends(get_current_active_user)
):  
    data = await consensus.get_multiple(ids, "sample_id")
    return data

@router.post("/", response_model=List[Consensus])
async def create_consensus_endpoint(
    obj_in: Consensus = Body(..., description="The consensus object to create"),
    current_user: User = Depends(get_current_active_user)
):
    data = await consensus.create(obj_in)
    return data

@router.put("/{id}")
async def update_consensus_endpoint(
    id: str,
    obj_in: Consensus,
    current_user: User = Depends(get_current_active_user)
):
    data = await consensus.update(id, obj_in, "sample_id")
    if data:
        return {f'{id}': 'updated successfully'}
    else:
        return {f'{id}': 'failed to update'}

@router.delete("/{id}", response_model=Consensus)
async def delete_consensus_endpoint(
    id: str,
    current_user: User = Depends(get_current_active_user)
):
    data = await consensus.delete(id, "sample_id")
    if data.deleted_count == 1:
        return {f'{id}': 'deleted successfully'}
    else:
        return {f'{id}': 'failed to delete'}