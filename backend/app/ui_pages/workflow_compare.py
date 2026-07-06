
import streamlit as st

from app.services.workflow_service import (
    WorkflowService
)

from app.services.workflow_version_service import (
    WorkflowVersionService
)

from app.services.workflow_diff_service import (
    WorkflowDiffService
)


def render():

    st.title(
        "🔍 Workflow Compare"
    )

    workflows = (
        WorkflowService
        .get_workflows()
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

    if len(versions) < 2:

        st.warning(
            "Need at least 2 versions."
        )

        return

    labels = [

        str(v["version_number"])

        for v in versions

    ]

    left = st.selectbox(
        "Version A",
        labels,
        key="left"
    )

    right = st.selectbox(
        "Version B",
        labels,
        key="right"
    )

    version_a = next(
        v
        for v in versions
        if str(v["version_number"])
        == left
    )

    version_b = next(
        v
        for v in versions
        if str(v["version_number"])
        == right
    )

    diff = (
        WorkflowDiffService
        .compare(
            version_a[
                "workflow_json"
            ],
            version_b[
                "workflow_json"
            ]
        )
    )

    st.subheader(
        "Added Nodes"
    )

    st.write(
        diff["added_nodes"]
    )

    st.subheader(
        "Removed Nodes"
    )

    st.write(
        diff["removed_nodes"]
    )

    st.subheader(
        "Added Edges"
    )

    st.write(
        diff["added_edges"]
    )

    st.subheader(
        "Removed Edges"
    )

    st.write(
        diff["removed_edges"]
    )
