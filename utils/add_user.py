#!/usr/bin/env python

# Temporary script to add users to the DB
# Planned removal of this script: 22-06-10
from pymongo import MongoClient
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError


def main():
    # Connect to the DB
    collection = MongoClient()["sarscov2_standalone"]["users"]
    # Ask for data to store
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    email = input("Enter email: ")
    fullname = input("Full name: ")
    
    pass_hash = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


    # Insert the user in the DB
    try:
        collection.insert_one({"_id":user,"username": user, "password": pass_hash, "email": email, "fullname": fullname, "disabled":False})
        print("User created.")
    except DuplicateKeyError:
        print("User already present in DB.")


if __name__ == '__main__':
    main()