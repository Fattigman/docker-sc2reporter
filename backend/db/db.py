import motor
from bson import json_util
import json

import os

client = motor.motor_tornado.MotorClient(os.getenv('MONGO_HOST'), 27017)


db = client['sarscov2_standalone']
        
def parse_json(data):
    return json.loads(json_util.dumps(data))