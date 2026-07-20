
from dataclasses import dataclass
from typing import List


@dataclass
class AgentDefinition:

    id: str | None

    user_id: str

    name: str

    description: str

    system_prompt: str

    provider: str

    model: str

    tools: List[str]

    memory_enabled: bool = False

    knowledge_enabled: bool = False

    active: bool = True
