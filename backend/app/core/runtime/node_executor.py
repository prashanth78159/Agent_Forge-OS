
from app.core.agents.agent_orchestrator import AgentOrchestrator

class NodeExecutor:

    def __init__(
        self,
        provider,
        api_key,
        model
    ):

        self.agent = AgentOrchestrator(
            provider,
            api_key,
            model
        )

    async def execute(
        self,
        node,
        context
    ):

        prompt = node.config.get(
            "prompt",
            ""
        )

        result = self.agent.run(
            prompt
        )

        return result
