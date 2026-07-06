
from app.config.database import db


class ExecutionStateService:

    @staticmethod
    def save_state(
        execution_id,
        current_node,
        status
    ):

        return (
            db.client
            .table(
                "workflow_execution_state"
            )
            .upsert(
                {
                    "execution_id":
                        execution_id,

                    "current_node":
                        current_node,

                    "status":
                        status
                }
            )
            .execute()
        )

    @staticmethod
    def get_state(
        execution_id
    ):

        result = (
            db.client
            .table(
                "workflow_execution_state"
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
