
from app.core.agents.agent_orchestrator import AgentOrchestrator


class AgentService:

    def __init__(self, api_key):
        self.orchestrator = AgentOrchestrator(
            api_key=api_key
        )

    def execute(self, task):
        return self.orchestrator.run(task)
