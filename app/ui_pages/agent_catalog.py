
import streamlit as st

def render():

    st.title(
        "🤖 Agent Catalog"
    )

    agents = [

        {
            "name":
                "Planner Agent",

            "role":
                "Planning",

            "status":
                "Online",

            "description":
                "Breaks a task into executable steps."
        },

        {
            "name":
                "Research Agent",

            "role":
                "Research",

            "status":
                "Online",

            "description":
                "Collects information and context."
        },

        {
            "name":
                "Writer Agent",

            "role":
                "Generation",

            "status":
                "Online",

            "description":
                "Produces content and responses."
        },

        {
            "name":
                "Critic Agent",

            "role":
                "Validation",

            "status":
                "Online",

            "description":
                "Reviews and improves outputs."
        }

    ]

    for agent in agents:

        with st.container():

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.markdown(
                    f"### {agent['name']}"
                )

                st.write(
                    f"Role: {agent['role']}"
                )

                st.write(
                    agent['description']
                )

            with col2:

                st.success(
                    agent["status"]
                )

            st.divider()
