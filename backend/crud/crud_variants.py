from .crud_base import CRUDBase
from models import Variant

# Handling of the variants collection


class CRUDVariant(CRUDBase):
    def __init__(self):
        super().__init__(Variant, "variant")


variants = CRUDVariant()
