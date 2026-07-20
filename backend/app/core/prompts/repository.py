
from app.services.database_service import get_db


class PromptRepository:

    def __init__(self):

        self.db = get_db()

    def create(
        self,
        payload
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .insert(payload)
            .execute()
        )

    def list_by_user(
        self,
        user_id
    ):

        return (
            self.db.client
            .table("prompt_templates")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

    def get_by_id(
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

    def update(
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

    def delete(
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
