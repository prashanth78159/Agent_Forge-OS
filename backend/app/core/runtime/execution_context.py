
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionContext:

    user_id: str

    workspace_id: Optional[str] = None

    workflow_id: Optional[str] = None

    agent_id: Optional[str] = None

    execution_id: Optional[str] = None
