
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


def render():

    st.title(
        "✅ Approval Center"
    )

    requests = (
        ApprovalService
        .get_requests()
    )

    if not requests:

        st.info(
            "No approvals pending."
        )

        return

    for row in requests:

        with st.expander(
            f"{row['node_id']} | {row['status']}"
        ):

            st.write(row)

            if row["status"] == "PENDING":

                if st.button(
                    f"Approve-{row['id']}"
                ):

                    ApprovalService.approve(
                        row["id"]
                    )

                    ExecutionStateService.save_state(

                        row["execution_id"],

                        row["node_id"],

                        "APPROVED"

                    )

                    WorkflowResumeService.mark_resumed(

                        row["execution_id"]

                    )

                    st.success(
                        "Workflow Approved"
                    )

                    st.rerun()
