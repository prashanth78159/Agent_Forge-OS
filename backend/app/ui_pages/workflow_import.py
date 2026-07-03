
import json
import streamlit as st

from app.services.workflow_service import WorkflowService

def render():

    st.title("📥 Import Workflow")

    uploaded = st.file_uploader(
        "Upload Workflow JSON",
        type=["json"]
    )

    if not uploaded:
        return

    data = json.load(uploaded)

    workflow_name = st.text_input(
        "Workflow Name",
        "Imported Workflow"
    )

    if st.button(
        "Import Workflow"
    ):

        WorkflowService.save_workflow(
            workflow_name,
            data
        )

        st.success(
            "Workflow Imported"
        )
