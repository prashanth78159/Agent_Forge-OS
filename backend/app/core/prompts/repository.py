
from typing import Dict, List


class PromptRepository:

    def __init__(self, supabase):
        self.supabase = supabase

    def create(self, payload: Dict):

        return (
            self.supabase
            .table("prompt_templates")
            .insert(payload)
            .execute()
        )

    def get_by_id(self, prompt_id: str):

        return (
            self.supabase
            .table("prompt_templates")
            .select("*")
            .eq("id", prompt_id)
            .single()
            .execute()
        )

    def get_by_user(self, user_id: str):

        return (
            self.supabase
            .table("prompt_templates")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

    def update(
        self,
        prompt_id: str,
        payload: Dict
    ):

        return (
            self.supabase
            .table("prompt_templates")
            .update(payload)
            .eq("id", prompt_id)
            .execute()
        )

    def delete(self, prompt_id: str):

        return (
            self.supabase
            .table("prompt_templates")
            .delete()
            .eq("id", prompt_id)
            .execute()
        )
