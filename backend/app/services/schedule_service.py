
from app.config.database import db


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
                        True
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
