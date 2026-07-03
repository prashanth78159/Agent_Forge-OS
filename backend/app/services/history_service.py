
from app.config.database import db


class HistoryService:

    @staticmethod
    def get_all_executions():

        try:

            result = (
                db.client
                .table("executions")
                .select("*")
                .execute()
            )

            return result.data

        except Exception as e:

            print(e)

            return []

    @staticmethod
    def get_logs(
        execution_id
    ):

        try:

            result = (
                db.client
                .table("execution_logs")
                .select("*")
                .eq(
                    "execution_id",
                    execution_id
                )
                .execute()
            )

            return result.data

        except Exception as e:

            print(e)

            return []
