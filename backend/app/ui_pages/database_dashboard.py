
import streamlit as st

from app.services.workflow_service import WorkflowService
from app.services.history_service import HistoryService

def render():

    st.title(
        "🗄 Database Dashboard"
    )

    workflows = (
        WorkflowService
        .get_workflows()
    )

    executions = (
        HistoryService
        .get_all_executions()
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Stored Workflows",
        len(workflows)
    )

    c2.metric(
        "Stored Executions",
        len(executions)
    )

    st.success(
        "Supabase Connected ✅"
    )
