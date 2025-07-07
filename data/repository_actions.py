from dataclasses import dataclass, field
from typing import List

@dataclass
class GitHubAction:
    name: str
    version: str        

@dataclass
class Workflow:
    name: str                         
    actions: List[GitHubAction] = field(default_factory=list)

@dataclass
class RepositoryActions:
    repository: str
    workflows: List[Workflow] = field(default_factory=list)
