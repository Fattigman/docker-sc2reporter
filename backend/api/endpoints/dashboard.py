from fastapi import APIRouter, Depends, HTTPException, Query
from crud.samples import *
from db import * 
from models import *
from authentication import *
from pprint import pprint
from typing import Literal

import time
import datetime

router = APIRouter()
@router.get("/", response_model=DashboardGraph)
async def get_dashboard_data(
    selection_criterion: list = Query([]),
    current_user: User = Depends(get_current_active_user)
):
    graph_list = await group_by_samples(selection_criterion)
    graph_list = fill_graph_data(graph_list)
    selection_criterions = await get_selection_criterions()
    general_stats = await get_general_stats()
    return {'general_stats':general_stats,'graph_list':graph_list, 'selection_criterions':selection_criterions}

def fill_graph_data(graph_list:list) -> list:
    dates = {}
    for graph in graph_list:
        if graph['date'] not in dates:
            dates[graph['date']] = [graph['pangolin']]
        else:
            dates[graph['date']].append(graph['pangolin'])
    pangolins = [item for sublist in dates.values() for item in sublist]
    for date in dates:
        for pangolin in pangolins:
            if pangolin not in dates[date]:
                graph_list.append({'date':date, 'pangolin':pangolin, 'pango_count':0})
    graph_list = sorted(graph_list, key=lambda k: k['date'])
    return graph_list