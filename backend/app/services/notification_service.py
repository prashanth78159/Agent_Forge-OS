
from app.config.database import db

from app.services.base_data_service import BaseDataService


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
                        BaseDataService
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
                BaseDataService.current_user_id()
            )
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data
