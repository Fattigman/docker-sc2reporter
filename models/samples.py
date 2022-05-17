from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

class Sample(BaseModel):
    sample_id : str
    qc : dict
    pct_N_bases: float
    sample_name: str
    num_aligned_reads: int
    pct_covered_bases: float
    longest_no_N_run: int
    on_target: float
    fasta: str
    variants: List[str]
    pangolin: dict