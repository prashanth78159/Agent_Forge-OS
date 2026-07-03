
import streamlit as st

def render(orchestrator):

    st.title("🚀 Agent Runner")

    if not orchestrator:
        st.warning(
            "Configure API Key first in Settings"
        )
        return

    task = st.text_area(
        "Task",
        height=200
    )

    if st.button("Run Agent"):

        if not task.strip():
            st.error("Task required")
            return

        try:

            with st.spinner(
                "Executing..."
            ):

                result = orchestrator.run(task)

                st.session_state[
                    "last_execution"
                ] = result

                st.success(
                    "Execution Completed"
                )

                st.subheader(
                    "Final Output"
                )

                st.markdown(
                    result["final"]
                )

        except Exception as e:

            st.error(str(e))
