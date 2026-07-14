from app.services.approval_service import (
    ApprovalService
)
from app.services.base_data_service import BaseDataService

class ApprovalRoutingService:

    GROUPS = {
        1: "Manager",
        2: "Director",
        3: "Finance"
    }

    MAX_LEVEL = 3

    @staticmethod
    def process_next_level(
        approval_row
    ):

        current_level = (
            approval_row.get(
                "approval_level",
                1
            )
        )

        if current_level >= (
            ApprovalRoutingService
            .MAX_LEVEL
        ):

            return {
                "final_level": True
            }

        next_level = (
            current_level + 1
        )

        ApprovalService.create_request(
            execution_id=
                approval_row[
                    "execution_id"
                ],

            node_id=
                approval_row[
                    "node_id"
                ],

            approval_level=
                next_level,

            approver_group=
                ApprovalRoutingService
                .GROUPS[
                    next_level
                ]
        )

        return {
            "final_level":
                False,

            "next_level":
                next_level
        }
