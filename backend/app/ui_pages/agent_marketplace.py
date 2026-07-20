
import streamlit as st

from app.services.agent_service import (
    AgentService
)


agent_service = AgentService()


def render(user):

    st.title("🤖 Agent Marketplace")

    create_tab, library_tab = st.tabs(
        [
            "Create Agent",
            "My Agents"
        ]
    )

    with create_tab:

        name = st.text_input(
            "Agent Name"
        )

        description = st.text_area(
            "Description"
        )

        system_prompt = st.text_area(
            "System Prompt",
            height=300
        )

        if st.button(
            "Create Agent"
        ):

            payload = {

                "user_id": user["id"],

                "name": name,

                "description": description,

                "system_prompt": system_prompt,

                "status": "DRAFT"
            }

            agent_service.create_agent(
                payload
            )

            st.success(
                "Agent Created"
            )

    with library_tab:

        response = (
            agent_service
            .list_agents(
                user["id"]
            )
        )

        agents = response.data or []

        for agent in agents:

            with st.expander(
                agent["name"]
            ):

                st.write(agent)
