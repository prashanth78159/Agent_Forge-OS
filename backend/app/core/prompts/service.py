
from app.core.prompts.repository import PromptRepository


class PromptService:

    def __init__(
        self,
        repository: PromptRepository
    ):
        self.repository = repository

    def create_prompt(
        self,
        user_id,
        name,
        description,
        category,
        prompt
    ):

        self.validate_prompt(prompt)

        payload = {
            "user_id": user_id,
            "name": name,
            "description": description,
            "category": category,
            "prompt": prompt,
            "version": 1,
            "status": "DRAFT"
        }

        return self.repository.create(payload)

    def get_prompt(
        self,
        prompt_id
    ):
        return self.repository.get_by_id(prompt_id)

    def get_user_prompts(
        self,
        user_id
    ):
        return self.repository.get_by_user(user_id)

    @staticmethod
    def validate_prompt(prompt):

        if not prompt:
            raise ValueError(
                "Prompt cannot be empty"
            )

        return True
