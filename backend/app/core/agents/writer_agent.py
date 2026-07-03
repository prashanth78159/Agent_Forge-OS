
from app.core.agents.base_agent import BaseAgent


class WriterAgent(BaseAgent):

    def run(
        self,
        input_text,
        context
    ):

        prompt = f'''
You are a writer agent.

Input:

{input_text}

Generate polished content.
'''

        return self._generate_and_log(
            prompt
        )
