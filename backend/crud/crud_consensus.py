from .crud_base import CRUDBase
from models import Consensus


class CRUDConsensus(CRUDBase):
    def __init__(self):
        super().__init__(Consensus, "consensus")


consensus = CRUDConsensus()
