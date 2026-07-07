
from app.config.database import db


class ExecutionSnapshotService:

    @staticmethod
    def save_snapshot(
        execution_id,
        workflow_json,
        outputs,
        completed_nodes
    ):

        return (
            db.client
            .table(
                "workflow_execution_snapshot"
            )
            .upsert(
                {
                    "execution_id":
                        execution_id,

                    "workflow_json":
                        workflow_json,

                    "outputs":
                        outputs,

                    "completed_nodes":
                        completed_nodes
                }
            )
            .execute()
        )

    @staticmethod
    def get_snapshot(
        execution_id
    ):

        result = (
            db.client
            .table(
                "workflow_execution_snapshot"
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
