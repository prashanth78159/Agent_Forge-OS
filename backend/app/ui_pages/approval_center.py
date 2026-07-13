
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

from app.services.auth_service import AuthService
from app.services.rbac_service import RBACService

from app.config.database import db

def render():
    print(f"DEBUG (approval_center.py): Entering render(). st object ID: {id(st)}")

    st.title(
        "✅ Approval Center"
    )

    # Get current user's roles
    current_user_roles = AuthService.get_user_roles()

    group_options = [
        "ALL",
        "Manager",
        "Director",
        "Finance"
    ]

    # Filter options based on user roles
    if "admin" not in current_user_roles:
        # If not an admin, only show groups they are part of
        allowed_groups = [g for g in group_options if g == "ALL" or g.lower() in current_user_roles]
        # Ensure 'ALL' is always an option if the user has any relevant role
        if not allowed_groups: # If no roles, no options, exit gracefully
            st.warning("You do not have any roles assigned to view approval groups.")
            return
        group_options = allowed_groups

    group_filter = st.selectbox(
        "Approver Group",
        group_options
    )

    requests = (
        ApprovalService
        .get_requests()
    )

    # Filter by selected group and user roles
    filtered_requests = []
    for r in requests:
        approver_group = r.get("approver_group")
        user_can_view_group = False

        if "admin" in current_user_roles: # Admins can view all
            user_can_view_group = True
        elif approver_group and approver_group.lower() in current_user_roles:
            user_can_view_group = True

        if user_can_view_group:
            if group_filter == "ALL" or (approver_group and approver_group == group_filter):
                filtered_requests.append(r)

    requests = filtered_requests

    if not requests:

        st.info(
            "No approvals pending for your roles or selected group."
        )

        return

    for row in requests:
        approver_group_for_row = row.get("approver_group")
        user_can_act = RBACService.has_role("admin") or (approver_group_for_row and RBACService.has_role(approver_group_for_row.lower()))

        with st.expander(
            f"{row['node_id']} | {row['status']} | Group: {approver_group_for_row if approver_group_for_row else 'N/A'}"
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
                    approver_group_for_row
            })

            comment = st.text_area(

                "Approval Comment",

                key=f"comment_{row['id']}"

            )

            if row["status"] == "PENDING":

                approve_button_disabled = not user_can_act
                reject_button_disabled = not user_can_act
                escalate_button_disabled = not user_can_act

                print(f"DEBUG (AC): Before Approve button {row['id']}: label='Approve-{row['id']}', disabled={approve_button_disabled}")
                approve_button_result = st.button(
                    f"Approve-{row['id']}",
                    disabled=approve_button_disabled
                )
                print(f"DEBUG (AC): Approve button result for {row['id']}: {approve_button_result}, disabled={approve_button_disabled}")

                if approve_button_result:

                    if not user_can_act:
                        st.warning("You do not have permission to approve this request.")
                        continue

                    try:
                        print("DEBUG (Approval Center): Approve button clicked. Starting approval process.")
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
                            print("DEBUG (Approval Center): Final level approval. Marking resumed and resuming execution.")
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
                            print(f"DEBUG (Approval Center): Intermediate level approval. Request sent for next level ({next_level_info['next_level']}).")
                            st.success(
                                f"✅ Approval for Level {row.get('approval_level', 1)} approved. Request sent for next level ({next_level_info['next_level']})."
                            )
                        print("DEBUG (Approval Center): About to call st.rerun()...")
                        st.rerun()

                    except Exception as e:
                        print(f"DEBUG (Approval Center): Exception in Approve button block: {e}")
                        st.error(
                            str(e)
                        )

                if st.button(

                    f"Reject-{row['id']}",
                    disabled=reject_button_disabled
                ):

                    if not user_can_act:
                        st.warning("You do not have permission to reject this request.")
                        continue

                    try:
                        print("DEBUG (Approval Center): Reject button clicked. Starting rejection process.")
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
                        print(f"DEBUG (Approval Center): Exception in Reject button block: {e}")
                        st.error(
                            str(e)
                        )

                if st.button(
                    f"Escalate-{row['id']}",
                    disabled=escalate_button_disabled
                ):

                    if not user_can_act:
                        st.warning("You do not have permission to escalate this request.")
                        continue
                    print("DEBUG (Approval Center): Escalate button clicked.")
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
