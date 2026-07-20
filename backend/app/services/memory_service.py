
from app.services.database_service import get_db


class MemoryService:

    def __init__(self):

        self.db = get_db()

    def store_memory(
        self,
        payload
    ):

        return (
            self.db.client
            .table("agent_memory")
            .insert(payload)
            .execute()
        )

    def get_agent_memory(
        self,
        agent_id
    ):

        return (
            self.db.client
            .table("agent_memory")
            .select("*")
            .eq("agent_id", agent_id)
            .order(
                "importance_score",
                desc=True
            )
            .execute()
        )

    def delete_memory(
        self,
        memory_id
    ):

        return (
            self.db.client
            .table("agent_memory")
            .delete()
            .eq("id", memory_id)
            .execute()
        )
