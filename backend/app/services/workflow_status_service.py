
from app.config.database import db


class WorkflowStatusService:

    @staticmethod
    def update_progress(
        execution_id,
        progress
    ):

        return (
            db.client
            .table(
                "workflow_executions"
            )
            .update(
                {
                    "progress": progress
                }
            )
            .eq(
                "id",
                execution_id
            )
            .execute()
        )

    @staticmethod
    def set_node_status(
        execution_id,
        node_name,
        status
    ):

        return (
            db.client
            .table(
                "workflow_node_status"
            )
            .insert(
                {
                    "execution_id":
                        execution_id,

                    "node_name":
                        node_name,

                    "status":
                        status
                }
            )
            .execute()
        )

    @staticmethod
    def get_status(
        execution_id
    ):

        result = (
            db.client
            .table(
                "workflow_node_status"
            )
            .select("*")
            .eq(
                "execution_id",
                execution_id
            )
            .execute()
        )

        return result.data
