
from app.services.database_service import get_db


class PromptService:

    def __init__(self):

        self.db = get_db()

    def list_prompts(
        self,
        user_id
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

    def get_prompt(
        self,
        prompt_id
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .select("*")
            .eq("id", prompt_id)
            .single()
            .execute()
        )

    def create_prompt(
        self,
        payload
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .insert(payload)
            .execute()
        )

    def update_prompt(
        self,
        prompt_id,
        payload
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .update(payload)
            .eq("id", prompt_id)
            .execute()
        )

    def publish_prompt(
        self,
        prompt_id
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .update(
                {
                    "status": "PUBLISHED"
                }
            )
            .eq("id", prompt_id)
            .execute()
        )

    def archive_prompt(
        self,
        prompt_id
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .update(
                {
                    "status": "ARCHIVED"
                }
            )
            .eq("id", prompt_id)
            .execute()
        )

    def delete_prompt(
        self,
        prompt_id
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .delete()
            .eq("id", prompt_id)
            .execute()
        )
