from fastapi import APIRouter, Depends, HTTPException, Query
from crud.samples import *
from db import * 
from models import *
from authentication import *

from typing import Literal

import time
import datetime

router = APIRouter()
@router.post("/", response_model=DashboardGraph)
async def get_dashboard_data(
    selection_criterion: list = Query([]),
    current_user: User = Depends(get_current_active_user)
):
    graph_list = await group_by_samples(selection_criterion)
    selection_criterions = await get_selection_criterions()
    general_stats = await get_general_stats()
    return {'general_stats':general_stats,'graph_list':graph_list, 'selection_criterions':selection_criterions}