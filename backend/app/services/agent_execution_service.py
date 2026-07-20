
from app.services.database_service import get_db


class AgentExecutionService:

    def __init__(self):

        self.db = get_db()

    def save_execution(
        self,
        payload
    ):

        return (
            self.db.client
            .table("agent_executions")
            .insert(payload)
            .execute()
        )

    def get_executions(
        self,
        user_id
    ):

        return (
            self.db.client
            .table("agent_executions")
            .select("*")
            .eq("user_id", user_id)
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )
