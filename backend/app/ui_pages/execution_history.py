
import streamlit as st
import pandas as pd

from app.services.history_service import (
    HistoryService
)

def render():

    st.title(
        "📜 Execution History"
    )

    rows = (
        HistoryService
        .get_all_executions()
    )

    if not rows:

        st.info(
            "No executions available."
        )

        return

    df = pd.DataFrame(rows)

    st.metric(
        "Total Executions",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.info(
        "Copy an execution ID and open Replay Viewer."
    )
