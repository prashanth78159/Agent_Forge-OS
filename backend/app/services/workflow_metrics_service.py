from app.config.database import db
from app.services.base_data_service import BaseDataService

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
        # Temporary Debug
        user_id = BaseDataService.current_user_id()
        print(f"DEBUG: WorkflowMetricsService - user_id found: {user_id}")

        return (
            db.client
            .table(
                "workflow_metrics"
            )
            .insert(
                {
                    "user_id": user_id,
                    "execution_id": execution_id,
                    "total_nodes": total_nodes,
                    "completed_nodes": completed_nodes,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "cost": cost
                }
            )
            .execute()
        )
