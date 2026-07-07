
import streamlit as st
from app.config.database import db
def render():
    st.title(
        "🚨 Approval Escalations"
    )
    rows = (
        db.client
        .table(
            "workflow_approvals"
        )
        .select("*")
        .eq(
            "escalated",
            True
        )
        .execute()
        .data
    )
    st.metric(
        "Escalated Approvals",
        len(rows)
    )
    st.dataframe(
        rows,
        use_container_width=True
    )
