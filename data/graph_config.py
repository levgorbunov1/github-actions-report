from dataclasses import dataclass
from typing import Optional
from pandas import DataFrame

@dataclass
class GraphConfig:
    source: DataFrame
    x: str
    y: str
    graph_type: str
    title: str
    color_separation_variable: Optional[str] = None 
    subplots_variable: Optional[str] = None
    output_path: Optional[str] = "graph.png"

