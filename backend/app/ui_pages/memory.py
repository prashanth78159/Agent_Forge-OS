
import streamlit as st

def render(orchestrator):

    st.title("🧠 Memory Explorer")

    if not orchestrator:

        st.warning(
            "No orchestrator"
        )

        return

    st.subheader(
        "Short Term Memory"
    )

    st.json(
        orchestrator.memory.sessions
    )

    st.divider()

    st.subheader(
        "Long Term Memory"
    )

    for item in (
        orchestrator
        .long_term_memory
        .store
    ):

        st.info(item)
