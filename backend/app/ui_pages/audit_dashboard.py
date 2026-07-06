
import pandas as pd
import streamlit as st

from app.services.audit_service import (
    AuditService
)


def render():

    st.title(
        "📜 Workflow Audit Trail"
    )

    rows = (
        AuditService
        .get_events()
    )

    if not rows:

        st.info(
            "No audit records found."
        )

        return

    df = pd.DataFrame(
        rows
    )

    st.metric(
        "Audit Events",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True
    )
