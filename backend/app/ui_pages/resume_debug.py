
import streamlit as st

from app.services.execution_snapshot_service import (
    ExecutionSnapshotService
)

from app.services.resume_dag_service import (
    ResumeDAGService
)
from app.services.resume_execution_service import (
    ResumeExecutionService
)


def render():

    st.title(
        "🔄 Resume Debug"
    )

    execution_id = st.text_input(
        "Execution ID"
    )

    if st.button(
        "Load Snapshot"
    ):

        snapshot = (
            ExecutionSnapshotService
            .get_snapshot(
                execution_id
            )
        )

        if not snapshot:

            st.error(
                "Snapshot not found"
            )

            return

        st.success(
            "Snapshot Loaded"
        )

        st.subheader(
            "Workflow JSON"
        )

        st.json(
            snapshot["workflow_json"]
        )

        st.subheader(
            "Outputs"
        )

        st.json(
            snapshot["outputs"]
        )

        st.subheader(
            "Completed Nodes"
        )

        st.json(
            snapshot["completed_nodes"]
        )

        remaining = (
            ResumeDAGService
            .get_remaining_nodes(
                execution_id
            )
        )

        st.subheader(
            "Remaining Nodes"
        )

        st.json(
            remaining
        )

    if st.button(
        "Simulate Resume"
    ):

        result = (
            ResumeExecutionService
            .resume_execution(
                execution_id
            )
        )

        st.json(
            result
        )



