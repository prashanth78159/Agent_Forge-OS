from app.config.database import db

from app.services.notification_service import (
    NotificationService
)

from app.services.base_data_service import BaseDataService

from datetime import (
    datetime,
    timedelta,
    timezone
)


class ApprovalService:

    @staticmethod
    def is_approval_node(
        node
    ):

        return (
            node.get(
                "type"
            )
            ==
            "approval"
        )

    @staticmethod
    def create_request(
        execution_id,
        node_id,
        approval_level=1,
        approver_group="Manager"
    ):

        existing = (
            db.client
            .table(
                "workflow_approvals"
            )
            .select("*")
            .eq(
                "execution_id",
                execution_id
            )
            .eq(
                "node_id",
                node_id
            )
            .eq(
                "status",
                "PENDING"
            )
            .execute()
        )

        if existing.data:

            return existing

        due_at = (
            datetime.now(
                timezone.utc
            )
            +
            timedelta(
                hours=24
            )
        )

        result = (
            db.client
            .table(
                "workflow_approvals"
            )
            .insert(
                {
                    "execution_id":
                        execution_id,

                    "node_id":
                        node_id,

                    "status":
                        "PENDING",

                    "approval_level":
                        approval_level,

                    "approver_group":
                        approver_group,

                    "due_at":
                        due_at.isoformat(),

                    "user_id":
                        BaseDataService.current_user_id()
                }
            )
            .execute()
        )

        NotificationService.create_notification(

            "Approval Required",

            f"Approval required for node {node_id}"

        )

        return result

    @staticmethod
    def get_requests():

        result = (
            db.client
            .table(
                "workflow_approvals"
            )
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data

    @staticmethod
    def approve(
        approval_id
    ):

        return (
            db.client
            .table(
                "workflow_approvals"
            )
            .update(
                {
                    "status":
                        "APPROVED",

                    "approved_at":
                        datetime.now(
                            timezone.utc
                        ).isoformat()
                }
            )
            .eq(
                "id",
                approval_id
            )
            .execute()
        )

    @staticmethod
    def reject(
        approval_id
    ):

        return (
            db.client
            .table(
                "workflow_approvals"
            )
            .update(
                {
                    "status":
                        "REJECTED"
                }
            )
            .eq(
                "id",
                approval_id
            )
            .execute()
        )

    @staticmethod
    def add_comment(
        approval_id,
        comment
    ):

        return (
            db.client
            .table(
                "workflow_approvals"
            )
            .update(
                {
                    "approval_comments":
                        comment
                }
            )
            .eq(
                "id",
                approval_id
            )
            .execute()
        )
