
import streamlit as st

from app.services.workspace_service import (
    WorkspaceService
)

from app.services.workspace_member_service import (
    WorkspaceMemberService
)


def render():

    st.title(
        "🏢 Workspaces"
    )

    name = st.text_input(
        "Workspace Name"
    )

    if st.button(
        "Create Workspace"
    ):

        WorkspaceService.create_workspace(
            name
        )

        st.success(
            "Workspace Created"
        )

        st.rerun()

    workspaces = (
        WorkspaceService
        .get_workspaces()
    )

    st.subheader(
        "My Workspaces"
    )

    for ws in workspaces:

        with st.expander(
            ws["name"]
        ):

            members = (
                WorkspaceMemberService
                .get_members(
                    ws["id"]
                )
            )

            st.write(
                members
            )
