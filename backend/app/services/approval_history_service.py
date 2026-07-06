
from app.config.database import db

from app.services.current_user_service import (
    CurrentUserService
)


class ApprovalHistoryService:

    @staticmethod
    def log_action(
        approval_id,
        action,
        comments=""
    ):

        return (
            db.client
            .table(
                "approval_history"
            )
            .insert(
                {
                    "approval_id":
                        approval_id,

                    "action":
                        action,

                    "comments":
                        comments,

                    "user_id":
                        CurrentUserService
                        .get_user_id()
                }
            )
            .execute()
        )

    @staticmethod
    def get_history(
        approval_id
    ):

        result = (
            db.client
            .table(
                "approval_history"
            )
            .select("*")
            .eq(
                "approval_id",
                approval_id
            )
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data
