
import json
import streamlit as st

from app.services.workflow_service import (
    WorkflowService
)

def render():

    st.title(
        "📤 Workflow Export Center"
    )

    workflows = (
        WorkflowService.get_workflows()
    )

    if not workflows:

        st.warning(
            "No workflows found."
        )

        return

    selected = st.selectbox(

        "Workflow",

        [w["name"] for w in workflows]
    )

    workflow = next(
        w for w in workflows
        if w["name"] == selected
    )

    st.download_button(

        "Export Workflow",

        json.dumps(
            workflow["workflow_json"],
            indent=2
        ),

        file_name=
            f"{selected}.json",

        mime=
            "application/json"
    )
