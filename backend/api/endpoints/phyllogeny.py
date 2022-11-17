from fastapi import APIRouter, Depends, HTTPException, Query

from models import User

from authentication import get_current_active_user
router = APIRouter()

@router.get("/")
def get_distances(
    current_user: User = Depends(get_current_active_user)
):
    return {'message':'Hello'}