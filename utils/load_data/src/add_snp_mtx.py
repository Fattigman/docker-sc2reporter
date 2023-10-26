# This will only be used to migrate from version 1.0.0 to 2.0.0
# This will be removed in future versions

# imports appropiate packages
import pandas as pd
import numpy as np
import pymongo
from tqdm import tqdm
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError
from pprint import pprint
from typing import List, Tuple
import os

from multiprocessing import Pool, cpu_count

db_name = os.getenv("MONGODB_NAME", "sarscov2_standalone")
host = os.getenv("MONGODB_HOST", "localhost")
port = os.getenv("MONGODB_PORT", 27017)
db = pymongo.MongoClient(host, port)[db_name]


def calculate_vector(name: str) -> Tuple[str, List[float]]:
    col = []
    index = set()
    # Chunk the data to avoid memory issues
    for i, ele in enumerate(db.depth.find({"sample_id": name})):
        temp = [ele["A"], ele["T"], ele["C"], ele["G"]]
        norm_temp = [x / max(temp) if max(temp) != 0 else np.nan for x in temp]
        for j, base in enumerate(["A", "T", "C", "G"]):
            idx = f"{ele['pos']}_{base}"
            if idx not in index:
                col.append(norm_temp[j])
                index.add(idx)
    return name, col


def insert_sample(sample: tuple) -> None:
    sample_name, array = sample
    try:
        db["matrix"].insert_one({"_id": sample_name, "array": array})
    except DuplicateKeyError:
        print(f"{sample_name} already exists in the database")


# creates the matrix
def create_matrix(db_name: str = "sarscov2_standalone") -> None:
    # Get all sample names to iterate over
    sample_names = [x["sample_id"] for x in db.sample.find({}, {"sample_id": 1})]
    print("Calculating matrix from depth collection...")
    pool = Pool(processes=os.getenv("PROCESSORS_AVAILABLE", int(cpu_count() / 2)))

    results = pool.map(calculate_vector, sample_names)
    names, arrays = zip(*results)
    df = pd.DataFrame(arrays)
    df = df.fillna(df.transpose().mean()).transpose()
    df.columns = names
    dict_df = df.to_dict("list")
    print("Inserting samples into matrix...")
    pool.map(insert_sample, dict_df.items())


# creates the superuser
def create_superuser(db_name: str = "sarscov2_standalone") -> str:
    db.users.drop()
    # create user collection
    db.create_collection("users")
    # create user
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)
    collection = db.users

    try:
        collection.insert_one(
            {
                "_id": "admin",
                "username": username,
                "password": hashed_password,
                "email": "admin@admin.com",
                "fullname": "Admin Adminson",
                "disabled": False,
                "scope": "admin",
            }
        )
        print(f"User created: {username}")
    except DuplicateKeyError:
        print("User already exists in the database")
    except Exception as e:
        print(e)
    return username


if __name__ == "__main__":
    print("Creating matrix...")
    create_matrix()
    # create_superuser()
