from typing import Optional

import motor
from bson import json_util
import json

import os

client = motor.motor_tornado.MotorClient(os.getenv('MONGO_HOST'), 27017)


db = client['sarscov2_standalone']
def get_db():
    return db
        
def parse_json(data):
    return json.loads(json_util.dumps(data)) 



# Handling of the user collection

async def get_user(username : str):
    curr =  db.users.find({"username": username})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    if len(docs) > 0:
        return  docs[0]
    else:
        return None

async def get_users():
    cursor =  db.users.find()
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)

# Handling of the depth collection
async def get_depth(query: Optional[any] = None):
    cursor =  db.depth.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)

# Handling of the variants collection

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

# Handling of the consensus collection

async def get_consensus(query: Optional[any] = None):
    cursor =  db.consensus.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)
