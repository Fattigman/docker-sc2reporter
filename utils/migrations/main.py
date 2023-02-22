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
# creates the matrix
def create_matrix(db_name:str='sarscov2_standalone'):

    db = pymongo.MongoClient('localhost',27017)[db_name]
    df = pd.DataFrame()

    # Get all sample names to iterate over
    sample_names = [x['sample_id'] for x in db.sample.find()]
    print ('Calculating matrix from depth collection...')
    for name in tqdm(sample_names):
        col = []
        index = []
        # Chunk the data to avoid memory issues
        for i, ele in enumerate(db.depth.find({'sample_id':name})):
            temp = [ele['A'], ele['T'], ele['C'], ele['G']]
            col.extend([x/max(temp)  if max(temp) != 0 else np.nan for x in temp] )
            index.extend([f'{ele["pos"]}_A', f'{ele["pos"]}_T', f'{ele["pos"]}_C', f'{ele["pos"]}_G'])
        df[name] = col

    df.index = index
    df = df.transpose().fillna(df.transpose().mean()).transpose()
    dict_df = df.to_dict('list')
    print ('Inserting samples into matrix...')
    for i, ele in enumerate(tqdm(dict_df)):
        try:
            db['matrix'].insert_one({
                '_id': ele,
                'array': dict_df[ele]
            })
        except DuplicateKeyError:
            print (f'{ele} already exists in the database')

# creates the superuser
def create_superuser(db_name:str='sarscov2_standalone'):
    db = pymongo.MongoClient('localhost',27017)[db_name]
    db.users.drop()
    # create user collection
    db.create_collection('users')
    # create user
    username = input('Enter username: ')
    password = input('Enter password: ')
    hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)
    collection = db.users

    try:
        collection.insert_one({
            "_id":'admin',
            "username": username,
            "password": hashed_password, 
            "email": 'admin@admin.com', 
            "fullname": 'Admin Adminson', 
            "disabled":False, 
            "scope":'admin'})
        print (f'User created: {username}')
    except DuplicateKeyError:
        print ('User already exists in the database')
    except Exception as e:
        print (e)
    return username

if __name__ == '__main__':
    print ('Creating matrix...')
    create_matrix()
    create_superuser()