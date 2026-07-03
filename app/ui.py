
import streamlit as st

from app.ui_pages.dashboard import render as dashboard_page
from app.ui_pages.agent_catalog import render as catalog_page
from app.ui_pages.workflow_builder import render as workflow_builder_page
from app.ui_pages.workflow_visualizer import render as workflow_visualizer_page
from app.ui_pages.agent_runner import render as agent_runner_page
from app.ui_pages.execution_center import render as execution_page
from app.ui_pages.replay import render as replay_page
from app.ui_pages.memory import render as memory_page
from app.ui_pages.metrics import render as metrics_page
from app.ui_pages.settings import render as settings_page
from app.ui_pages.contact import render as contact_page

st.set_page_config(
    page_title="AgentForge OS",
    page_icon="🚀",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "stored_workflows" not in st.session_state:
    st.session_state.stored_workflows = {}

if not st.session_state.logged_in:

    st.title("🔐 AgentForge")

    user = st.text_input(
        "Username"
    )

    pwd = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if user == "admin" and pwd == "admin":

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error(
                "Invalid credentials"
            )

    st.stop()

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Agent Catalog",
        "Agent Runner",
        "Workflow Builder",
        "Workflow Visualizer",
        "Execution Center",
        "Replay",
        "Memory",
        "Metrics",
        "Settings",
        "Contact"
    ]
)

orchestrator = st.session_state.get(
    "orchestrator"
)

if menu == "Dashboard":
    dashboard_page(
        orchestrator,
        st.session_state.stored_workflows
    )

elif menu == "Agent Catalog":
    catalog_page()

elif menu == "Agent Runner":
    agent_runner_page(
        orchestrator
    )

elif menu == "Workflow Builder":
    workflow_builder_page()

elif menu == "Workflow Visualizer":
    workflow_visualizer_page(
        st.session_state.stored_workflows
    )

elif menu == "Execution Center":
    execution_page()

elif menu == "Replay":
    replay_page(
        orchestrator
    )

elif menu == "Memory":
    memory_page(
        orchestrator
    )

elif menu == "Metrics":
    metrics_page(
        orchestrator
    )

elif menu == "Settings":
    settings_page()

elif menu == "Contact":
    contact_page()
