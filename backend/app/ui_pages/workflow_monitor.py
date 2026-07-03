
import streamlit as st

from app.services.workflow_status_service import (
    WorkflowStatusService
)

def render():

    st.title(
        "📡 Workflow Monitor"
    )

    execution_id = st.text_input(
        "Execution ID"
    )

    if not execution_id:
        return

    rows = (
        WorkflowStatusService
        .get_status(
            execution_id
        )
    )

    if not rows:

        st.info(
            "No status found."
        )

        return

    for row in rows:

        st.write(
            f"{row['node_name']} → {row['status']}"
        )
