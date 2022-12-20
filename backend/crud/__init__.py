"""
This module contains all the CRUD functions for the database.
The functions are imported in the endpoints and used to interact with the database.
Create a new file for each collection in the database, and export them here.
"""
from .crud_users import get_users, get_user, del_user, create_user
from .crud_matrix import get_matrix
from .crud_samples import get_samples, get_single_sample, delete_single_sample, delete_multiple_samples, get_general_stats, group_by_samples, get_selection_criterions
from .crud_variants import get_variants, get_single_variant, get_multiple_variants