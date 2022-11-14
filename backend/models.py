from pydantic import BaseModel
from typing import Union, Literal


class Pangolin(BaseModel):
    conflict: Union[int, str]
    type: str
    pangolearn_version: str

class Variant(BaseModel):
    dp: int
    aa: str
    id: str
    alt_freq: float

class DashBoardGraphElement(BaseModel):
    date: str
    pango_count: int
    pangolin: str

class SimpleGraphElement(BaseModel):
    date: str
    count: int



class GeneralStats(BaseModel):
    passed_qc_samples: int
    unique_pangos: int
    unique_mutations: int

class DashboardGraph(BaseModel):
    graph_list: list[DashBoardGraphElement]
    general_stats: GeneralStats
    selection_criterions: list[str]


class Sample(BaseModel):
    _id: dict
    variants : Union[list[Variant],None] = None
    qc: dict
    time_added: dict
    pangolin: Pangolin
    nextclade: str
    vcf_filename: Union[str, None]
    depth_filename: Union[str, None]
    sample_id: str
    age: Union[str, None]
    collection_date: Union[dict, None]
    lab: Union[str, None]
    mlu: Union[str, None]
    selection_criterion: Union[str, None]
    sex: Union[str, None]
    Ct: Union[str, None]
    similar_samples: Union[list, None]
    

class GroupedSamples(BaseModel):
    samples: list[Sample]
    graph: list[SimpleGraphElement]
class Basic_User(BaseModel):
    username: str 
    email: str
    fullname: str
    disabled: bool = False
    scope: Literal['user','admin']

class User(Basic_User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(User):
    hashed_password: str