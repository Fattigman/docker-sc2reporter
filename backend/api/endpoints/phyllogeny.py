from fastapi import APIRouter, Depends, HTTPException, Query

from models import User

from typing import List

from collections import defaultdict

import time
from crud import samples

import random
from authentication import get_current_active_user

from skbio import DistanceMatrix
from skbio.tree import nj
from db import * 
router = APIRouter()

@router.get("/")
async def get_distances(
    current_user: User = Depends(get_current_active_user),
    group: str = Query(..., description="The group to get the distances for (try 'samples')"),
    sample_list: List[str] = Query(..., description="The list of samples to get the distances for (need at least 3 samples)")
    ):
    if group == 'samples':
        curr = db.sample.find(
            {'sample_id': 
            {'$in': sample_list }
            })
        samples =  [parse_json(x) for x in await curr.to_list(None)]
        if len(samples) < 3:
            return {"error": "Not enough samples to create a tree"}
    else:
        return {"error": "Invalid group"}


    presence = defaultdict(set)
    all_samples = set()
    sample_metadata = {}
    pango_color = {}
    nextstrain_color = {}

    r = lambda: random.randint(0, 255)

    for sample in samples:
        if "collection_date" not in sample:
            continue

        for var in sample.get("variants", []):
            presence[var["id"]].add(sample["sample_id"])

        all_samples.add(sample["sample_id"])

        pango_type = sample["pangolin"]["type"]
        nextstrain_clade = sample.get("nextclade")

        # Generate random color for new pango types
        if pango_type not in pango_color:
            pango_color[pango_type] = '#%02X%02X%02X' % (r(), r(), r())

        if nextstrain_clade not in nextstrain_color:
            nextstrain_color[nextstrain_clade] = '#%02X%02X%02X' % (
                r(), r(), r())

        date = time.strftime('%Y-%m-%d', time.localtime(sample.get("collection_date")['$date']))

        sample_metadata[sample.get('sample_id')] = {
            'year': date.split('-')[0],
            'month': date.split('-')[1],
            'day': date.split('-')[2],
            'country': "Sweden",
            'pango': pango_type,
            'pango__color': pango_color[pango_type],
            'nextstrain': nextstrain_clade,
            'nextstrain__color': nextstrain_color[nextstrain_clade],
            'country__color': "#358",
            'time': date
            }



    distance = defaultdict(dict)

    for s1 in all_samples:
        for s2 in all_samples:
            distance[s1][s2] = 0

    for var_id, samples_with_variant in presence.items():
        samples_without_variant = all_samples ^ samples_with_variant
        for s_without in samples_without_variant:
            for s_with in samples_with_variant:
                distance[s_without][s_with] += 1
                distance[s_with][s_without] += 1

    data = []
    for s in all_samples:
        data.append(list(distance[s].values()))

    ids = list(all_samples)
    dm = DistanceMatrix(data, ids)
    tree = nj(dm, result_constructor = str)

    tree = {'nwk':tree}
    tree['metadata'] = sample_metadata

    
    metaLista = set()
    for key in sample_metadata:
        for key2 in sample_metadata[key]:
            metaLista.add(key2)
    metaLista = list(metaLista) 
    tree['metadata_list'] = metaLista
    tree['metadata_options'] = {"time":{"label":"time","coltype":"character","grouptype":"alphabetic","colorscheme":"gradient"}}
    
    options = dict()
    length = 0

    for key in tree['metadata']:
        if len(tree['metadata'][key]) > length: longest_obj = key
        
    for ele in tree['metadata_list']:
        try: 
            data_type = int(tree['metadata'][longest_obj][ele])
            data_type = 'gradient'
        except Exception as e:
            data_type = 'category'
        options[ele] = {"label": ele, "coltype":"character", "grouptype":"alphabetic", "colorscheme":data_type}
    tree['metadata_options'] = options
    return  tree

