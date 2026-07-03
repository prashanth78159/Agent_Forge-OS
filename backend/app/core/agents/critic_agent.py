
from app.core.agents.base_agent import BaseAgent


class CriticAgent(BaseAgent):

    def run(
        self,
        input_text,
        context
    ):

        prompt = f'''
You are a critic agent.

Review:

{input_text}

Improve and refine the output.
'''

        return self._generate_and_log(
            prompt
        )
