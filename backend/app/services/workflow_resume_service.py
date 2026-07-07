
from app.config.database import db


class WorkflowResumeService:

    @staticmethod
    def mark_resumed(
        execution_id
    ):

        return (
            db.client
            .table(
                "workflow_execution_state"
            )
            .update(
                {
                    "status":
                        "RESUMED"
                }
            )
            .eq(
                "execution_id",
                execution_id
            )
            .execute()
        )
