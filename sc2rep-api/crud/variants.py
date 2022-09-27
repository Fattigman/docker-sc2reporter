
from db import * 

async def get_variants(query: Optional[any] = None):
    cursor =  db.variant.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)

async def get_single_variant(variant_id : str):
    curr =  db.variant.find({"sample_id": variant_id})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_multiple_variants(variant_ids):
    curr =  db.variant.find({"sample_id": {'$in': variant_ids}})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs