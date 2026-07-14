
from app.config.database import db
from app.services.base_data_service import BaseDataService

class AuditService:
    @staticmethod
    def log_event(workflow_id, event_type, event_details=""):
        return (
            db.client
            .table("workflow_audit_log")
            .insert({
                "user_id": BaseDataService.current_user_id(),
                "workflow_id": workflow_id,
                "event_type": event_type,
                "event_details": event_details
            })
            .execute()
        )

    @staticmethod
    def get_events():
        result = (
            db.client
            .table("workflow_audit_log")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return result.data
