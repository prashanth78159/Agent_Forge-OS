
from app.config.database import db


class WorkflowHistoryService:

    @staticmethod
    def get_executions():

        result = (
            db.client
            .table("workflow_executions")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data

    @staticmethod
    def get_outputs(
        execution_id
    ):

        result = (
            db.client
            .table("workflow_node_outputs")
            .select("*")
            .eq(
                "workflow_execution_id",
                execution_id
            )
            .execute()
        )

        return result.data
