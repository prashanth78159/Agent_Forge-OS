
from app.services.database_service import get_db


class AgentPlaygroundService:

    def __init__(self):

        self.db = get_db()

    def save_message(
        self,
        payload
    ):

        return (
            self.db.client
            .table("agent_conversations")
            .insert(payload)
            .execute()
        )

    def get_conversation(
        self,
        agent_id
    ):

        return (
            self.db.client
            .table("agent_conversations")
            .select("*")
            .eq("agent_id", agent_id)
            .order("created_at", desc=True)
            .execute()
        )
