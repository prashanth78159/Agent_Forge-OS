
from app.config.database import db

class WorkflowExecutionService:

    @staticmethod
    def save_execution(
        execution_id,
        workflow_id,
        status
    ):

        return (
            db.client
            .table("workflow_executions")
            .insert(
                {
                    "id": execution_id,
                    "workflow_id": workflow_id,
                    "status": status
                }
            )
            .execute()
        )

    @staticmethod
    def save_output(
        execution_id,
        node_id,
        output
    ):

        return (
            db.client
            .table("workflow_node_outputs")
            .insert(
                {
                    "workflow_execution_id":
                        execution_id,

                    "node_id":
                        node_id,

                    "output_data":
                        str(output)
                }
            )
            .execute()
        )
