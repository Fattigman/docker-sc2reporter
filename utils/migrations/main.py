# This will only be used to migrate from version 1.0.0 to 2.0.0
# This will be removed in future versions

# imports appropiate packages
import pandas as pd
import numpy as np
import pymongo

from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

# creates the matrix
def create_matrix():
    db = pymongo.MongoClient('localhost',27017).sarscov2_standalone
    samples = [x for x in db.sample.find()]
    variants = [x for x in db.variant.find()]
    depth = [x for x in db.depth.find()]

    df = pd.DataFrame()
    col_name = ''
    col = []
    index = []
    for i, ele in enumerate(depth):
        if i == 0:
            col_name = ele['sample_id']
        if ele['sample_id'] != col_name:
            df[col_name] = col
            col_name = ele['sample_id']
            col = []
            index = []
        temp = [ele['A'], ele['T'], ele['C'], ele['G']]
        col.extend([x/max(temp)  if max(temp) != 0 else np.nan for x in temp] )
        index.extend([f'{ele["pos"]}_A', f'{ele["pos"]}_T', f'{ele["pos"]}_C', f'{ele["pos"]}_G'])
        
    df.index = index
        
    df = df.transpose().fillna(df.transpose().mean()).transpose()

    dict_df = df.to_dict('list')
    db['matrix'].insert_one(dict_df)

# creates the superuser
def create_superuser():
    db = pymongo.MongoClient('localhost',27017).sarscov2_standalone
    db.users.drop()
    # create user collection
    db.create_collection('users')
    hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash('<YOUR_PASSWORD>')
    db_user = 'admin'
    collection = db.users

    try:
        collection.insert_one({
            "_id":'admin',
            "username": 'admin', 
            "password": hashed_password, 
            "email": 'admin@admin.com', 
            "fullname": 'Admin Adminson', 
            "disabled":False, 
            "scope":'admin'})
        print("User created.")
    except DuplicateKeyError:
        print ('User already exists in the database')
    return db_user

if __name__ == '__main__':
    create_matrix()
    create_superuser()