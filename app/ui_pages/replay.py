
import streamlit as st

def render(orchestrator):

    st.title("🔁 Replay Center")

    if not orchestrator:
        st.warning(
            "Orchestrator unavailable"
        )
        return

    executions = list(
        orchestrator.store.executions.keys()
    )

    if not executions:
        st.info(
            "No executions yet"
        )
        return

    selected = st.selectbox(
        "Execution",
        executions
    )

    if st.button(
        "Replay Execution"
    ):

        logs = (
            orchestrator.store.get(
                selected
            )
        )

        for log in logs:

            with st.expander(
                log["step"]
            ):

                st.write(
                    "Input"
                )

                st.write(
                    log["input"]
                )

                st.write(
                    "Output"
                )

                st.write(
                    log["output"]
                )
