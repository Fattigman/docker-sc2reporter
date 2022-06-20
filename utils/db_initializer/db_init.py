import pymongo
# Check if the database exists
# Delete the database if it exists
client = pymongo.MongoClient('localhost',27017)
db_name = 'sarscov2_standalone'
if db_name in client.list_database_names():
    print(f'{db_name} exists and will be deleted')
    if input(f'Do you want to delete {db_name}: (y/n) ') == 'y':
        client.drop_database(f'{db_name}')
else:
    print(f'{db_name} does not exist')