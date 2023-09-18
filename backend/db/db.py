import motor
from bson import json_util
import json
import os
from api.config import settings

"""
This is meant to be imported by the other crud files.
The idea is to have a single place where the database is defined.
Import this file in the other crud files and use the db object.
"""

client = motor.motor_tornado.MotorClient(
    host=os.getenv("MONGO_HOST"),
    port=os.getenv("MONGO_PORT"),
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASS"),
)
db = client[settings.DATABASE_NAME]


def parse_json(data):
    return json.loads(json_util.dumps(data))
