
from supabase import create_client

from app.config.database import (
    SUPABASE_URL,
    SUPABASE_KEY
)


class DatabaseService:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.client = create_client(
                SUPABASE_URL,
                SUPABASE_KEY
            )

        return cls._instance

    def save_execution(
        self,
        execution_id,
        status,
        workflow_id=None
    ):

        return (
            self.client
            .table("workflow_executions")
            .upsert(
                {
                    "id": execution_id,
                    "status": status,
                    "workflow_id": workflow_id
                }
            )
            .execute()
        )

    def get_execution(
        self,
        execution_id
    ):

        return (
            self.client
            .table("workflow_executions")
            .select("*")
            .eq("id", execution_id)
            .single()
            .execute()
        )


def get_db():

    return DatabaseService()
