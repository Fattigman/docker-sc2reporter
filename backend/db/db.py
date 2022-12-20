import motor
from bson import json_util
import json
import os

"""
This is meant to be imported by the other crud files.
The idea is to have a single place where the database is defined.
Import this file in the other crud files and use the db variable.
"""

client = motor.motor_tornado.MotorClient(os.getenv('MONGO_HOST'), 27017)
db = client['sarscov2_standalone']
        
def parse_json(data):
    return json.loads(json_util.dumps(data))