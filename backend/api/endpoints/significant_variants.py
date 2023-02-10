from fastapi import APIRouter, Depends, HTTPException, status, Depends
from crud import significant_variants as crud
from models import *
from authentication import *


router = APIRouter()

# Gets all samples 
@router.get("/")
async def get_significant_variants(
    current_user: User = Depends(get_current_active_user),
    ): 
    variants = await crud.get()
    return variants

@router.post("/")
async def create_significant_variants(
    variant: SignificantVariant,
    current_user: User = Depends(get_current_active_user),
    ):
    if current_user['scope'] == 'user':
        raise HTTPException(status_code=403, detail="Not allowed")
    create_response = await crud.create(variant)
    return create_response

@router.put("/")
async def update_significant_variants(
    variant: SignificantVariant,
    current_user: User = Depends(get_current_active_user),
    ):
    if current_user['scope'] == 'user':
        raise HTTPException(status_code=403, detail="Not allowed")
    update_response = await crud.update(variant)
    return update_response