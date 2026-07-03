
from dataclasses import dataclass
from dataclasses import field

@dataclass
class Workflow:

    id: str
    name: str

    nodes: list = field(default_factory=list)
    edges: list = field(default_factory=list)
