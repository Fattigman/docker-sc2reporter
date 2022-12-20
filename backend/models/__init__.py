"""
This folder contains the models for the database.
The models are used to define the structure of the data.
They are also used to define the structure of the responses.
Import them into endpoints and use them for responses and inputs.
"""
from .sample import Sample, GroupedSamples, Variant, Pangolin
from .user import User, Basic_User
from .graph import SimpleGraphElement, DashBoardGraphElement, GeneralStats, DashboardGraph
from .login import Token, TokenData, UserInDB