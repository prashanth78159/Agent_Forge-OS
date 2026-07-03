
import streamlit as st
import pandas as pd

from app.services.workflow_history_service import (
    WorkflowHistoryService
)

def render():

    st.title(
        "📜 Workflow Execution History"
    )

    rows = (
        WorkflowHistoryService
        .get_executions()
    )

    if not rows:

        st.info(
            "No workflow executions found."
        )

        return

    df = pd.DataFrame(
        rows
    )

    st.metric(
        "Total Workflow Executions",
        len(df)
    )

    st.dataframe(
        df,
        width="stretch"
    )
