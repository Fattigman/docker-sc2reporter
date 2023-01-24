from .crud_base import CRUDBase
from models import Depth

# Handling of the depth collection
class CRUDDepth(CRUDBase[Depth, Depth]):
    def __init__(self):
        super().__init__(Depth, "depth")

depth = CRUDDepth()