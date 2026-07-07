
from app.config.database import db

from app.services.notification_service import (
    NotificationService
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
        node_id
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
                        "PENDING"
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
                        "APPROVED"
                }
            )
            .eq(
                "id",
                approval_id
            )
            .execute()
        )
