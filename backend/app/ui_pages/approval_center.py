
import streamlit as st

from app.services.approval_service import (
    ApprovalService
)

from app.services.execution_state_service import (
    ExecutionStateService
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

            st.write(
                row
            )

            if (
                row["status"]
                ==
                "PENDING"
            ):

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

                    st.success(
                        "Approved"
                    )

                    st.rerun()
