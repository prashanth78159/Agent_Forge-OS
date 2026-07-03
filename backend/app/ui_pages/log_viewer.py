
import streamlit as st

from app.services.history_service import (
    HistoryService
)

def render():

    st.title("📄 Execution Replay")

    execution_id = st.text_input(
        "Execution ID"
    )

    if not execution_id:
        return

    logs = (
        HistoryService
        .get_logs(
            execution_id
        )
    )

    if not logs:

        st.warning(
            "No logs found."
        )

        return

    st.success(
        f"Loaded {len(logs)} logs"
    )

    for idx, log in enumerate(logs):

        st.subheader(
            f"Step {idx+1}: {log['step']}"
        )

        st.write("### Input")

        st.code(
            str(
                log["input_data"]
            )
        )

        st.write("### Output")

        st.code(
            str(
                log["output_data"]
            )
        )

        st.divider()
