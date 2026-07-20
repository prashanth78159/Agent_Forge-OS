
from app.core.prompts.repository import PromptRepository


class PromptService:

    def __init__(self):

        self.repository = PromptRepository()

    def create_prompt(
        self,
        user_id,
        name,
        description,
        category,
        prompt
    ):

        payload = {

            "user_id": user_id,

            "name": name,

            "description": description,

            "category": category,

            "prompt": prompt,

            "version": 1,

            "status": "DRAFT"
        }

        return self.repository.create(
            payload
        )

    def get_prompt(
        self,
        prompt_id
    ):

        return self.repository.get_by_id(
            prompt_id
        )

    def list_prompts(
        self,
        user_id
    ):

        return self.repository.list_by_user(
            user_id
        )

    def update_prompt(
        self,
        prompt_id,
        payload
    ):

        return self.repository.update(
            prompt_id,
            payload
        )

    def delete_prompt(
        self,
        prompt_id
    ):

        return self.repository.delete(
            prompt_id
        )
