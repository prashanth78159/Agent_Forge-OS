
from app.config.database import db

from app.services.current_user_service import (
    CurrentUserService
)


class WorkflowExecutionService:

    @staticmethod
    def save_execution(
        execution_id,
        workflow_id,
        status
    ):

        return (
            db.client
            .table(
                "workflow_executions"
            )
            .insert(
                {
                    "id":
                        execution_id,

                    "workflow_id":
                        workflow_id,

                    "status":
                        status,

                    "user_id":
                        CurrentUserService
                        .get_user_id()
                }
            )
            .execute()
        )

    @staticmethod
    def save_output(
        execution_id,
        node_id,
        output
    ):

        return (
            db.client
            .table(
                "workflow_node_outputs"
            )
            .insert(
                {
                    "workflow_execution_id":
                        execution_id,

                    "node_id":
                        node_id,

                    "output_data":
                        str(output)
                }
            )
            .execute()
        )

    @staticmethod
    def get_executions():

        return (
            db.client
            .table(
                "workflow_executions"
            )
            .select("*")
            .eq(
                "user_id",
                CurrentUserService
                .get_user_id()
            )
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )
