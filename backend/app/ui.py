
import streamlit as st

from app.ui_pages.dashboard import render as dashboard_page

from app.ui_pages.agent_catalog import render as agent_catalog_page
from app.ui_pages.agent_runner import render as agent_runner_page

from app.ui_pages.workflow_builder import render as workflow_builder_page
from app.ui_pages.workflow_visualizer import render as workflow_visualizer_page
from app.ui_pages.workflow_library import render as workflow_library_page

from app.ui_pages.workflow_marketplace import render as workflow_marketplace_page
from app.ui_pages.workflow_import import render as workflow_import_page
from app.ui_pages.save_template import render as save_template_page

from app.ui_pages.workflow_executor import render as workflow_executor_page
from app.ui_pages.workflow_execution_history import render as workflow_execution_history_page
from app.ui_pages.workflow_replay import render as workflow_replay_page
from app.ui_pages.workflow_generator import render as workflow_generator_page

from app.ui_pages.execution_center import render as execution_center_page
from app.ui_pages.execution_history import render as execution_history_page
from app.ui_pages.execution_search import render as execution_search_page
from app.ui_pages.log_viewer import render as log_viewer_page

from app.ui_pages.memory import render as memory_page
from app.ui_pages.metrics import render as metrics_page

from app.ui_pages.profile import render as profile_page
from app.ui_pages.api_vault import render as api_vault_page
from app.ui_pages.settings import render as settings_page
from app.ui_pages.contact import render as contact_page

from app.ui_pages.database_dashboard import render as database_dashboard_page

st.set_page_config(
    page_title="AgentForge OS",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# LOGIN
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🚀 AgentForge OS")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login"
    ):

        if (
            username == "admin"
            and
            password == "admin"
        ):

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error(
                "Invalid credentials"
            )

    st.stop()

# ==========================================
# SIDEBAR
# ==========================================

menu = st.sidebar.radio(

    "Navigation",

    [

        "Dashboard",

        "Agent Catalog",
        "Agent Runner",

        "Workflow Builder",
        "Workflow Visualizer",
        "Workflow Library",

        "Workflow Marketplace",
        "Workflow Import",
        "Save Template",

        "Workflow Executor",
        "Workflow Execution History",
        "Workflow Replay",

        "AI Workflow Generator",

        "Execution Center",
        "Execution History",
        "Execution Search",
        "Log Viewer",

        "Memory",
        "Metrics",

        "Database Dashboard",

        "Profile",
        "API Vault",
        "Settings",
        "Contact"
    ]
)

orchestrator = st.session_state.get(
    "orchestrator"
)

stored_workflows = st.session_state.get(
    "stored_workflows",
    {}
)

# ==========================================
# ROUTER
# ==========================================

if menu == "Dashboard":

    dashboard_page(
        orchestrator,
        stored_workflows
    )

elif menu == "Agent Catalog":

    agent_catalog_page()

elif menu == "Agent Runner":

    agent_runner_page(
        orchestrator
    )

elif menu == "Workflow Builder":

    workflow_builder_page()

elif menu == "Workflow Visualizer":

    workflow_visualizer_page(
        stored_workflows
    )

elif menu == "Workflow Library":

    workflow_library_page()

elif menu == "Workflow Marketplace":

    workflow_marketplace_page()

elif menu == "Workflow Import":

    workflow_import_page()

elif menu == "Save Template":

    save_template_page()

elif menu == "Workflow Executor":

    workflow_executor_page()

elif menu == "Workflow Execution History":

    workflow_execution_history_page()

elif menu == "Workflow Replay":

    workflow_replay_page()

elif menu == "AI Workflow Generator":

    workflow_generator_page()

elif menu == "Execution Center":

    execution_center_page()

elif menu == "Execution History":

    execution_history_page()

elif menu == "Execution Search":

    execution_search_page()

elif menu == "Log Viewer":

    log_viewer_page()

elif menu == "Memory":

    memory_page(
        orchestrator
    )

elif menu == "Metrics":

    metrics_page(
        orchestrator
    )

elif menu == "Database Dashboard":

    database_dashboard_page()

elif menu == "Profile":

    profile_page()

elif menu == "API Vault":

    api_vault_page()

elif menu == "Settings":

    settings_page()

elif menu == "Contact":

    contact_page()
