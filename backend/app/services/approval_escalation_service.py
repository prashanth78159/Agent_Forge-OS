
from datetime import (
    datetime,
    timezone
)
from app.config.database import db
from app.services.notification_service import (
    NotificationService
)
class ApprovalEscalationService:
    @staticmethod
    def process_overdue_approvals():
        approvals = (
            db.client
            .table(
                "workflow_approvals"
            )
            .select("*")
            .eq(
                "status",
                "PENDING"
            )
            .eq(
                "escalated",
                False
            )
            .execute()
            .data
        )
        now = datetime.now(
            timezone.utc
        )
        for row in approvals:
            due_at = row.get(
                "due_at"
            )
            if not due_at:
                continue
            try:
                due = datetime.fromisoformat(
                    due_at
                )
                if due < now:
                    db.client.table(
                        "workflow_approvals"
                    ).update(
                        {
                            "escalated":
                                True
                        }
                    ).eq(
                        "id",
                        row["id"]
                    ).execute()
                    NotificationService.create_notification(
                        "Approval Escalated",
                        f"Approval for {row['node_id']} is overdue."
                    )
            except Exception:
                pass
