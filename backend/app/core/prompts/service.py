
from app.core.prompts.models import PromptTemplate


class PromptService:

    @staticmethod
    def create_prompt(
        user_id: str,
        name: str,
        description: str,
        category: str,
        prompt: str
    ) -> PromptTemplate:

        return PromptTemplate(
            id=None,
            user_id=user_id,
            name=name,
            description=description,
            category=category,
            prompt=prompt
        )

    @staticmethod
    def validate_prompt(prompt: str):

        if not prompt:
            raise ValueError("Prompt cannot be empty")

        if len(prompt.strip()) == 0:
            raise ValueError("Prompt cannot be blank")

        return True
