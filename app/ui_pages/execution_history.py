
import streamlit as st
import pandas as pd

def render(orchestrator):

    st.title(
        "📜 Execution History"
    )

    if not orchestrator:
        return

    rows = []

    for execution_id, logs in (
        orchestrator.store.executions.items()
    ):

        rows.append(
            {
                "Execution":
                    execution_id,

                "Steps":
                    len(logs)
            }
        )

    if rows:

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True
        )
