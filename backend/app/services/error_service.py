
from app.config.database import db

from app.services.notification_service import (
    NotificationService
)


class ErrorService:

    @staticmethod
    def log_error(
        execution_id,
        node_id,
        error_message
    ):

        NotificationService.create_notification(

            "Workflow Failure",

            f"{node_id}: {error_message}"

        )

        return (
            db.client
            .table(
                "workflow_errors"
            )
            .insert(
                {
                    "execution_id":
                        execution_id,

                    "node_id":
                        node_id,

                    "error_message":
                        str(error_message)
                }
            )
            .execute()
        )

    @staticmethod
    def get_errors():

        result = (
            db.client
            .table(
                "workflow_errors"
            )
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data
