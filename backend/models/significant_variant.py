from pydantic import BaseModel

class SignificantVariant(BaseModel):
    variants : list
    pango_lineages : list
    positions : list
    virus_name: str = 'SARS-CoV-2'