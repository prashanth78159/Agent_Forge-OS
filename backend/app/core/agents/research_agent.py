
from app.core.agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):

    def run(
        self,
        input_text,
        context
    ):

        prompt = f'''
You are a research agent.

Topic:

{input_text}

Provide detailed findings.
'''

        return self._generate_and_log(
            prompt
        )
