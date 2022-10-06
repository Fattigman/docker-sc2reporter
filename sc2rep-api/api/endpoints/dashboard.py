from fastapi import APIRouter, Depends, HTTPException, Query
from db import *
from models import *
from authentication import *

import time
import datetime

router = APIRouter()


@router.get("/", response_model=DashboardGraph)
async def get_dashboard(
    current_user: User = Depends(get_current_active_user)
    ):
    samples = await get_samples()
    graph_list = list()

    for sample in samples:
        if 'collection_date' in sample.keys():
            sample_time = (time.strftime('%Y-%m-%d', time.localtime(sample['collection_date']['$date']/1000))) # convert epoch to datetime
            sample_pango = sample['pangolin']['type']
            if sample_pango == 'None': sample_pango = 'Undetermined'
            if len(graph_list) == 0: graph_list.append({'date':sample_time, 'value': 0, 'pangolin': sample_pango})
            else:
                for counter, graph_obj in enumerate(graph_list):
                    if graph_obj['date'] == sample_time and graph_obj['pangolin'] == sample_pango: 
                        graph_obj['value'] += 1
                        counter -= 1
                        break
                    elif counter+1 == len(graph_list):
                        graph_list.append({'date':sample_time, 'value': 1, 'pangolin': sample_pango})
        else: print(f'{sample["sample_id"]} doesnt have collection_date ')
    return {'plot_data':graph_list}