from .crud_base import CRUDBase
from models import SignificantVariant

# Handling of the depth collection
class CRUDSignificantVariants(CRUDBase[SignificantVariant, SignificantVariant]):
    def __init__(self):
        super().__init__(SignificantVariant, "significant_variants")

significant_variants = CRUDSignificantVariants()