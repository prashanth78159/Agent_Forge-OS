
import pandas as pd
import streamlit as st

from app.services.error_service import (
    ErrorService
)


def render():

    st.title(
        "🔁 Retry Dashboard"
    )

    rows = (
        ErrorService.get_errors()
    )

    if not rows:

        st.success(
            "No failures detected."
        )

        return

    df = pd.DataFrame(
        rows
    )

    st.metric(
        "Failures",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True
    )
