"""
This module contains all the CRUD functions for the database.
The functions are imported in the endpoints and used to interact with the database.
Create a new file for each collection in the database, and export them here.
"""
from .crud_users import get_users, get_user, del_user, create_user
from .crud_matrix import get_matrix
from .crud_samples import samples
from .crud_variants import variants
from .crud_depth import depth
from .crud_consensus import consensus
from .crud_significant_variants import significant_variants