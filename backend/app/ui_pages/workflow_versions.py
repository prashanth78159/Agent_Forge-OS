
import json
import streamlit as st

from app.services.workflow_service import (
    WorkflowService
)

from app.services.workflow_version_service import (
    WorkflowVersionService
)

from app.services.workflow_rollback_service import (
    WorkflowRollbackService
)


def render():

    st.title(
        "🕘 Workflow Versions"
    )

    workflows = (
        WorkflowService.get_workflows()
    )

    if not workflows:

        st.info(
            "No workflows found."
        )

        return

    workflow_name = st.selectbox(

        "Workflow",

        [
            w["name"]
            for w in workflows
        ]

    )

    workflow = next(

        w

        for w in workflows

        if w["name"]
        ==
        workflow_name

    )

    versions = (
        WorkflowVersionService
        .get_versions(
            str(workflow["id"])
        )
    )

    if not versions:

        st.info(
            "No versions found."
        )

        return

    for version in versions:

        with st.expander(

            f"Version {version['version_number']}"

        ):

            st.code(

                json.dumps(
                    version[
                        "workflow_json"
                    ],
                    indent=2
                ),

                language="json"
            )

            if st.button(

                f"Restore Version "
                f"{version['version_number']}"

            ):

                WorkflowRollbackService.restore_version(

                    str(
                        workflow["id"]
                    ),

                    version[
                        "workflow_json"
                    ]

                )

                st.success(
                    "Version Restored"
                )

                st.rerun()
