
import streamlit as st

def render():

    st.title("📊 Execution Timeline")

    execution = st.session_state.get(
        "last_execution"
    )

    if not execution:

        st.info(
            "Run an agent first"
        )

        return

    logs = execution["logs"]

    for index, log in enumerate(logs):

        st.markdown(
            f'''
### Step {index+1}

**Stage:** {log["step"]}
'''
        )

        st.success(
            "Completed"
        )

        st.divider()
