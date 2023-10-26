from fastapi import APIRouter, Depends, HTTPException, status, Depends, Body
from crud import significant_variants as crud
from models import *
from typing import List
from authentication import *

"""
Allows the user to change significant variants by inserting a list of desired variants.
If collection doesn't exist during first startup, it will be created based on the config.py file.
"""
router = APIRouter()


# Gets all samples
@router.get("/", response_model=list[SignificantVariant])
async def get_significant_variants(
    current_user: User = Depends(get_current_active_user),
):
    variants = await crud.get()
    return variants


@router.put("/")
async def update_significant_variants(
    field: str = Body(..., description="The field to update"),
    update: List[str] = Body(..., description="The value to update the field with"),
    current_user: User = Depends(get_current_active_user),
):
    if current_user["scope"] == "user":
        raise HTTPException(status_code=403, detail="Not allowed")
    update_response = await crud.patch(
        "significant_variants",
        SignificantVariant,
        patch_field=field,
        patch_value=update,
    )
    return update_response
