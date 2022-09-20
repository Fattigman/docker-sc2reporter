from pydantic import BaseModel
from typing import Union


class Pangolin(BaseModel):
    conflict: Union[int, str]
    type: str
    pangolearn_version: str

class Variant(BaseModel):
    dp: int
    aa: str
    id: str
    alt_freq: float


class Sample(BaseModel):
    _id: dict
    variants : Union[list[Variant],None] = None
    qc: dict
    time_added: dict
    pangolin: Pangolin
    nextclade: str
    vcf_filename: str
    depth_filename: str
    sample_id: str
    age: Union[str, None]
    collection_date: Union[dict, None]
    lab: Union[str, None]
    mlu: Union[str, None]
    selection_criterion: Union[str, None]
    sex: Union[str, None]
    Ct: Union[str, None]
    
class User(BaseModel):
    username: str 
    email: str
    fullname: str
    disabled: bool = False
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(User):
    hashed_password: str