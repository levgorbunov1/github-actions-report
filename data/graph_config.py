from dataclasses import dataclass
from typing import Optional
from pandas import DataFrame

@dataclass
class GraphConfig:
    source: DataFrame
    x: str
    y: str
    title: str
    graph_type: Optional[str] = None
    color_separation_variable: Optional[str] = None 
    subplots_variable: Optional[str] = None
    output_path: Optional[str] = "graph.png"

