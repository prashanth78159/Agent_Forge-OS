from app.config.database import db
from app.services.base_data_service import BaseDataService


class ScheduleService:

    @staticmethod
    def create_schedule(
        workflow_id,
        cron_expression
    ):

        return (
            db.client
            .table(
                "workflow_schedules"
            )
            .insert(
                {
                    "workflow_id":
                        workflow_id,

                    "cron_expression":
                        cron_expression,

                    "enabled":
                        True,

                    "user_id":
                        BaseDataService.current_user_id()
                }
            )
            .execute()
        )

    @staticmethod
    def get_schedules():

        result = (
            db.client
            .table(
                "workflow_schedules"
            )
            .select("*")
            .execute()
        )

        return result.data
