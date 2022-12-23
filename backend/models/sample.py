from pydantic import BaseModel
from typing import Union, Literal

from .graph import SimpleGraphElement

"""
Here we define the models for the samples
and the data associated with them.
"""

class Pangolin(BaseModel):
    #Pangolin classification of a sample
    conflict: Union[int, str]
    type: str
    pangolearn_version: str

class Variant(BaseModel):
    # Variant detection of a sample
    dp: int
    aa: str
    id: str
    alt_freq: float

class Sample(BaseModel):
    # SarsCov2 sample
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

class Consensus(BaseModel):
    _id : str
    sample_oid: str
    seq: str
    qual: str
    sample_id: str