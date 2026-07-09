

import streamlit as st

from app.services.approval_service import (
    ApprovalService
)

from app.services.execution_state_service import (
    ExecutionStateService
)

from app.services.workflow_resume_service import (
    WorkflowResumeService
)

from app.services.resume_execution_service import (
    ResumeExecutionService
)

from app.services.approval_routing_service import (
    ApprovalRoutingService
)

from app.config.database import db

def render():

    st.title(
        "✅ Approval Center"
    )

    group_filter = st.selectbox(
        "Approver Group",
        [
            "ALL",
            "Manager",
            "Director",
            "Finance"
        ]
    )

    requests = (
        ApprovalService
        .get_requests()
    )

    if group_filter != "ALL":
        requests = [
            r
            for r in requests
            if r.get(
                "approver_group"
            )
            ==
            group_filter
        ]

    if not requests:

        st.info(
            "No approvals pending."
        )

        return

    for row in requests:

        with st.expander(

            f"{row['node_id']} | {row['status']}"

        ):

            st.write({
                "Execution ID":
                    row["execution_id"],

                "Node":
                    row["node_id"],

                "Status":
                    row["status"],

                "Level":
                    row.get(
                        "approval_level"
                    ),

                "Group":
                    row.get(
                        "approver_group"
                    )
            })

            comment = st.text_area(

                "Approval Comment",

                key=f"comment_{row['id']}"

            )

            if row["status"] == "PENDING":

                if st.button(

                    f"Approve-{row['id']}"

                ):

                    try:

                        if hasattr(
                            ApprovalService,
                            "add_comment"
                        ):

                            ApprovalService.add_comment(

                                row["id"],

                                comment

                            )

                        ApprovalService.approve(

                            row["id"]

                        )

                        ExecutionStateService.save_state(
                            row["execution_id"],
                            row["node_id"],
                            "APPROVED"
                        )

                        next_level_info = ApprovalRoutingService.process_next_level(
                            row
                        )

                        if next_level_info["final_level"]:
                            WorkflowResumeService.mark_resumed(
                                row["execution_id"]
                            )
                            result = ResumeExecutionService.resume_execution(
                                row["execution_id"]
                            )
                            st.success(
                                "✅ Workflow Approved And Resumed"
                            )
                            st.json(
                                result
                            )
                        else:
                            st.success(
                                f"✅ Approval for Level {row.get('approval_level', 1)} approved. Request sent for next level ({next_level_info['next_level']})."
                            )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            str(e)
                        )

                if st.button(

                    f"Reject-{row['id']}"

                ):

                    try:

                        if hasattr(
                            ApprovalService,
                            "add_comment"
                        ):

                            ApprovalService.add_comment(

                                row["id"],

                                comment

                            )

                        ApprovalService.reject(

                            row["id"]

                        )

                        ExecutionStateService.save_state(

                            row["execution_id"],

                            row["node_id"],

                            "REJECTED"

                        )

                        st.warning(
                            "❌ Workflow Rejected"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            str(e)
                        )

                if st.button(
                    f"Escalate-{row['id']}"
                ):
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
                    st.success(
                        "Approval Escalated"
                    )
