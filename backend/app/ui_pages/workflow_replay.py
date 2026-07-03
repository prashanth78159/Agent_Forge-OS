
import streamlit as st

from app.services.workflow_history_service import (
    WorkflowHistoryService
)

def render():

    st.title(
        "🔁 Workflow Replay"
    )

    execution_id = st.text_input(
        "Execution ID"
    )

    if not execution_id:
        return

    outputs = (
        WorkflowHistoryService
        .get_outputs(
            execution_id
        )
    )

    if not outputs:

        st.warning(
            "No outputs found."
        )

        return

    for output in outputs:

        st.subheader(
            output["node_id"]
        )

        st.write(
            output["output_data"]
        )
