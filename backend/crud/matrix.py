from db import *

async def get_matrix(query: Optional[any] = None):
    cursor =  db.matrix.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)