from dataclasses import dataclass

@dataclass
class GitHubAction:
    repository: str
    workflow: str
    name: str
    version: str 
