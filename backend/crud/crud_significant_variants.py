from .crud_base import CRUDBase
from models import Depth

# Handling of the depth collection
class CRUDSignificantVariants(CRUDBase[Depth, Depth]):
    def __init__(self):
        super().__init__(Depth, "depth")

significant_variants = CRUDSignificantVariants()