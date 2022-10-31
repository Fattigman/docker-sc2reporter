from fastapi import APIRouter, Depends, HTTPException, Query
from crud.samples import *
from db import * 
from models import *
from authentication import *

import time
import datetime

router = APIRouter()


def create_general_stats(samples: list, graph_list:list, mutations: set):
    general_stats = dict()
    passed_qc = [s for s in samples if s['qc']['qc_pass'] == 'TRUE']
    unique_pangos = set([p['pangolin'] for p in graph_list if p['pangolin'] != 'Undetermined'])
    general_stats['passed_qc_samples'], general_stats['unique_pangos'] = len(passed_qc), len(unique_pangos)
    general_stats['unique_mutations'] = len(mutations)
    return general_stats

def create_graph_obj(samples: list):
    graph_list = list()
    mutations = set()
    for sample in samples:
        if 'collection_date' and 'variants' in sample.keys():
            sample_time = (time.strftime('%Y-%m-%w', time.localtime(sample['collection_date']['$date']/1000))) # convert epoch to datetime
            sample_pango = sample['pangolin']['type']
            [mutations.add(x['id']) for x in sample['variants']]
            if sample_pango == 'None': sample_pango = 'Undetermined'
            if len(graph_list) == 0: graph_list.append({'date':sample_time, 'pango_count': 0, 'pangolin': sample_pango})
            else:
                for counter, graph_obj in enumerate(graph_list):
                    if graph_obj['date'] == sample_time and graph_obj['pangolin'] == sample_pango: 
                        graph_obj['pango_count'] += 1
                        counter -= 1
                        break
                    elif counter+1 == len(graph_list):
                        graph_list.append({'date':sample_time, 'pango_count': 1, 'pangolin': sample_pango})
        else: print(f'{sample["sample_id"]} doesnt have collection_date or variant data')
    graph_list = sorted(graph_list,key=lambda d: d['date'])
    return graph_list, mutations


@router.get("/",
 response_model=DashboardGraph
 )
async def get_dashboard(current_user: User = Depends(get_current_active_user)):
    samples = await get_samples()
    
    graph_list, mutations = create_graph_obj(samples)

    general_stats = create_general_stats(samples, graph_list, mutations)

    return {'dashboard_data':graph_list, 'general_stats': general_stats}