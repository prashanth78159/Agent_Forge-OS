from app.config.database import db
from app.services.current_user_service import CurrentUserService


class WorkflowResumeService:

    @staticmethod
    def queue_resume(
        execution_id,
        workflow_id,
        approval_node
    ):

        existing = (
            db.client
            .table(
                "workflow_resume_queue"
            )
            .select("*")
            .eq(
                "execution_id",
                execution_id
            )
            .execute()
        )

        if existing.data:

            return existing.data[0]

        result = (
            db.client
            .table(
                "workflow_resume_queue"
            )
            .insert(
                {
                    "execution_id":
                        execution_id,

                    "workflow_id":
                        workflow_id,

                    "approval_node":
                        approval_node,

                    "status":
                        "WAITING",

                    "user_id":
                        CurrentUserService.get_user_id()
                }
            )
            .execute()
        )

        return result.data[0]

    @staticmethod
    def mark_resumed(
        execution_id
    ):

        return (
            db.client
            .table(
                "workflow_resume_queue"
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

    @staticmethod
    def get_resume_request(
        execution_id
    ):

        result = (
            db.client
            .table(
                "workflow_resume_queue"
            )
            .select("*")
            .eq(
                "execution_id",
                execution_id
            )
            .execute()
        )

        if result.data:

            return result.data[0]

        return None

    @staticmethod
    def get_node_outputs(
        execution_id
    ):

        result = (
            db.client
            .table(
                "workflow_node_outputs"
            )
            .select("*")
            .eq(
                "workflow_execution_id",
                execution_id
            )
            .execute()
        )

        return result.data
