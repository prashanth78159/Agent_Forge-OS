
from app.config.database import db
from app.services.workflow_resume_service import WorkflowResumeService


class HealthCheckService:

    @staticmethod
    def check_database_connection():
        try:
            db.client.postgrest.from_("workflows").select("id").limit(1).execute()
            return True, "Connected"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def check_table_accessibility(table_name):
        try:
            # Attempt to query a small amount of data to ensure accessibility
            db.client.postgrest.from_(table_name).select("id").limit(1).execute()
            return True, f"Accessible (Table: {table_name})"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_recent_workflow_executions(limit=10):
        try:
            result = (
                db.client
                .table("workflow_executions")
                .select("id, status, created_at, workflow_id")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return result.data
        except Exception:
            return []

    @staticmethod
    def get_pending_approvals_count():
        try:
            result = (
                db.client
                .table("workflow_approvals")
                .select("count")
                .eq("status", "PENDING")
                .execute()
            )
            return result.count
        except Exception:
            return 0

    @staticmethod
    def get_resume_engine_status():
        try:
            # Check for any queued resume requests
            result = (
                db.client
                .table("workflow_resume_queue")
                .select("count")
                .execute()
            )
            if result.count > 0:
                return "Active" # Or 'Pending Resumes' if more specific
            return "Idle"
        except Exception:
            return "Error"


