from db import *

# Handling of the depth collection
async def get_depth(query: Optional[any] = None):
    cursor =  db.depth.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)



# Handling of the consensus collection

async def get_consensus(query: Optional[any] = None):
    cursor =  db.consensus.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return (docs)
