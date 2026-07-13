
from supabase import create_client


class DatabaseService:

    def __init__(
        self,
        url,
        key
    ):
        self.client = create_client(
            url,
            key
        )

    def save_execution(
        self,
        execution_id,
        status,
        workflow_id=None
    ):

        return (
            self.client
            .table(
                "workflow_executions"
            )
            .upsert(
                {
                    "id":
                        execution_id,

                    "status":
                        status,

                    "workflow_id":
                        workflow_id
                }
            )
            .execute()
        )

    def get_execution(self, execution_id):

        return (
            self.client
            .table("workflow_executions")
            .select("*")
            .eq("id", execution_id)
            .single()
            .execute()
        )
