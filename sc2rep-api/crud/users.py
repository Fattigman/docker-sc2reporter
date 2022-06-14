from typing import List, Optional

from models import User

from pymongo import MongoClient
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

def create_user(db, user):
    hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(users.password)
    db_user = User(
        username=user.username,
        fullname=user.fullname,
        disable=False
        email=user.email, 
        hashed_password=hashed_password
        )


    try:
        collection.insert_one({"_id":user,"username": user, "password": pass_hash, "email": email, "fullname": fullname, "disabled":False})
        print("User created.")
    except DuplicateKeyError:
        print("User already present in DB.")
    return db_user