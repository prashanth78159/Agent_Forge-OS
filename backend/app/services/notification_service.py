
from app.config.database import db

from app.services.current_user_service import (
    CurrentUserService
)


class NotificationService:

    @staticmethod
    def create_notification(
        title,
        message
    ):

        return (
            db.client
            .table(
                "notifications"
            )
            .insert(
                {
                    "user_id":
                        CurrentUserService
                        .get_user_id(),

                    "title":
                        title,

                    "message":
                        message
                }
            )
            .execute()
        )

    @staticmethod
    def get_notifications():

        result = (
            db.client
            .table(
                "notifications"
            )
            .select("*")
            .eq(
                "user_id",
                CurrentUserService.get_user_id()
            )
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data
