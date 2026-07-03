
import streamlit as st
from app.services.workflow_service import WorkflowService

def render():

    st.title("📚 Workflow Library")

    workflows = WorkflowService.get_workflows()

    if not workflows:
        st.info("No workflows found.")
        return

    st.metric(
        "Total Workflows",
        len(workflows)
    )

    for workflow in workflows:

        name = workflow.get(
            "name",
            "Unnamed Workflow"
        )

        data = workflow.get(
            "workflow_json",
            {}
        )

        with st.expander(name):

            st.json(data)
