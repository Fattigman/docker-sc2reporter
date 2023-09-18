from db import *
from typing import Optional

"""
Reads the SNP matrix from the database.
Is used to efficeintly calculate phylogenetic distance.
"""


async def get_matrix(query: Optional[any] = None):
    cursor = db.matrix.find(query)
    docs = [parse_json(x) for x in await cursor.to_list(None)]
    return docs
