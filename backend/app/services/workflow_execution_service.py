from app.config.database import db
from app.services.base_data_service import BaseDataService

class WorkflowExecutionService:

    @staticmethod
    def save_execution(execution_id, workflow_id, status):
        user_id = BaseDataService.current_user_id()
        return (
            db.client
            .table("workflow_executions")
            .insert({
                "id": execution_id,
                "workflow_id": workflow_id,
                "status": status,
                "user_id": user_id
            })
            .execute()
        )

    @staticmethod
    def save_output(workflow_execution_id, node_id, output_data):
        user_id = BaseDataService.current_user_id()
        return (
            db.client
            .table("workflow_node_outputs")
            .insert({
                "workflow_execution_id": workflow_execution_id,
                "node_id": node_id,
                "output_data": output_data,
                "user_id": user_id
            })
            .execute()
        )

    @staticmethod
    def get_execution(execution_id):
        return (
            db.client
            .table("workflow_executions")
            .select("*")
            .eq("id", execution_id)
            .single()
            .execute()
        )
