from typing import List, Optional

from models import User

from pymongo import MongoClient
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

from db import get_db

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