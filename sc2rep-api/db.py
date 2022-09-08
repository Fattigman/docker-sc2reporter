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

async def get_samples(query: Optional[any] = None):
    cursor =  db.sample.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)


async def get_single_sample(sample_id : str):
    curr =  db.sample.find({"sample_id": sample_id})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_multiple_samples(sample_ids):
    curr =  db.sample.find({"sample_id": {'$in': sample_ids}})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs

async def get_user(username : str):
    curr =  db.users.find({"username": username})
    docs = [parse_json(x) for x in await curr.to_list(None)]
    return  docs[0]

async def get_users():
    cursor =  db.users.find()
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)

async def get_depth(query: Optional[any] = None):
    cursor =  db.depth.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)

async def get_variants(query: Optional[any] = None):
    cursor =  db.variant.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)

async def get_consensus(query: Optional[any] = None):
    cursor =  db.consensus.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)
