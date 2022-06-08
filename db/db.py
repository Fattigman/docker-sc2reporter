#from parso import parse
import motor
from bson.json_util import dumps
from bson import json_util
import json


MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_tornado.MotorClient('localhost', 27017)


db = client['sarscov2_standalone']

def parse_json(data):
    return json.loads(json_util.dumps(data)) 

async def get_all_samples():
    cursor =  db.sample.find()
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)


async def get_single_sample(sample_id : str):
    curr =  db.sample.find({"sample_id": sample_id})
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