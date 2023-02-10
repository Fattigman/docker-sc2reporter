from pydantic import BaseModel

class SignificantVariant(BaseModel):
    variants : list
    virus_name: str = 'SARS-CoV-2'