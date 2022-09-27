from typing import List, Optional

from models import User

from pymongo import MongoClient
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

from db import *

from fastapi import HTTPException, status

def create_user(user):
    db = get_db()
    hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password)
    db_user = user
    collection = db.users

    try:
        print('test')
        collection.insert_one({"_id":db_user.username,"username": db_user.username, "password": hashed_password, "email": db_user.email, "fullname": db_user.fullname, "disabled":False})
        print("User created.")
    except DuplicateKeyError:
        print ('User already exists in the database')
    return db_user

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