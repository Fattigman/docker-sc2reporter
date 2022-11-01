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





# Handling of the depth collection
async def get_depth(query: Optional[any] = None):
    cursor =  db.depth.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)



# Handling of the consensus collection

async def get_consensus(query: Optional[any] = None):
    cursor =  db.consensus.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)
