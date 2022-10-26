from db import *
#  Handling of the samples collection

async def get_samples(query: Optional[any] = None):
    cursor =  db.sample.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)

async def get_single_sample(sample_id : str):
    curr =  db.sample.find({"sample_id": sample_id})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_multiple_samples(sample_ids: list):
    curr =  db.sample.find({"sample_id": {'$in': sample_ids}})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_pangotype_samples(pangolin:str):
    curr =  db.sample.find({"pangolin.type": pangolin})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_variant_samples(variant:str):
    curr =  db.sample.find({"variants.id" : variant})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_nextclade_samples(nextclade:str):
    curr =  db.sample.find({"nextclade": nextclade})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs