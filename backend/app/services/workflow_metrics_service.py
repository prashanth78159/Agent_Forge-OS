
from app.config.database import db


class WorkflowMetricsService:

    @staticmethod
    def save_metrics(
        execution_id,
        total_nodes,
        completed_nodes,
        prompt_tokens,
        completion_tokens,
        cost
    ):

        return (

            db.client

            .table(
                "workflow_metrics"
            )

            .insert(
                {
                    "execution_id":
                        execution_id,

                    "total_nodes":
                        total_nodes,

                    "completed_nodes":
                        completed_nodes,

                    "prompt_tokens":
                        prompt_tokens,

                    "completion_tokens":
                        completion_tokens,

                    "cost":
                        cost
                }
            )

            .execute()

        )
