
from app.config.database import db

from app.services.audit_service import (
    AuditService
)


class WorkflowRollbackService:

    @staticmethod
    def restore_version(
        workflow_id,
        workflow_json
    ):

        result = (
            db.client
            .table(
                "workflows"
            )
            .update(
                {
                    "workflow_json":
                        workflow_json
                }
            )
            .eq(
                "id",
                workflow_id
            )
            .execute()
        )

        AuditService.log_event(

            workflow_id,

            "ROLLBACK",

            "Workflow restored to previous version"

        )

        return result
