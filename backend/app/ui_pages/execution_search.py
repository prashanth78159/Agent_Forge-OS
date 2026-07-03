
import streamlit as st

from app.services.history_service import HistoryService

def render():

    st.title(
        "🔍 Execution Search"
    )

    query = st.text_input(
        "Execution ID"
    )

    if not query:
        return

    executions = (
        HistoryService
        .get_all_executions()
    )

    results = []

    for execution in executions:

        if query.lower() in (
            execution["id"]
            .lower()
        ):

            results.append(
                execution
            )

    if results:

        st.success(
            f"Found {len(results)} result(s)"
        )

        st.write(results)

    else:

        st.warning(
            "No matching executions."
        )
