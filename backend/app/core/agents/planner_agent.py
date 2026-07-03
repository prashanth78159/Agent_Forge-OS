
from app.core.agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):

    def run(
        self,
        input_text,
        context
    ):

        prompt = f'''
You are a planner agent.

Task:

{input_text}

Create a clear step-by-step plan.
'''

        return self._generate_and_log(
            prompt
        )
