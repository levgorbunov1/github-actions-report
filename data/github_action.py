from dataclasses import dataclass

@dataclass
class GitHubAction:
    repository: str
    workflow: str
    name: str
    version: str 
    latest: bool

@dataclass
class GitHubActionTag:
    tag: str
    sha: str
    name: str