from pydantic import BaseModel

"""
Here we put the models which are to used for the graph objects.
They are designed to be compatible with the ant-design node package.
"""

class DashBoardGraphElement(BaseModel):
    date: str
    pango_count: int
    pangolin: str

class SimpleGraphElement(BaseModel):
    date: str
    count: int

class GeneralStats(BaseModel):
    passed_qc_samples: int
    unique_pangos: int
    unique_mutations: int

class DashboardGraph(BaseModel):
    dashboard_data: list[DashBoardGraphElement]
    general_stats: GeneralStats
    selection_criterions: list[str]