
import pandas as pd
import streamlit as st

from app.services.error_service import (
    ErrorService
)


def render():

    st.title(
        "🚨 Error Dashboard"
    )

    rows = (
        ErrorService
        .get_errors()
    )

    if not rows:

        st.success(
            "No workflow errors found."
        )

        return

    df = pd.DataFrame(
        rows
    )

    st.metric(
        "Total Errors",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    for row in rows:

        with st.expander(

            f"{row['node_id']} | "
            f"{row['created_at']}"

        ):

            st.code(
                row[
                    "error_message"
                ]
            )
