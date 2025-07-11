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

@dataclass
class NetworkGraphConfig:
    source: DataFrame
    root_node: str
    layer_1: str
    layer_2: str
    title: str
    color_separation_variable: Optional[str] = None 
    output_path: Optional[str] = "network_graph.png"