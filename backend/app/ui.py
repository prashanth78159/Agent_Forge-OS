
import streamlit as st

from app.ui_pages.auth_page import render as auth_page

from app.ui_pages.dashboard import render as dashboard_page
from app.ui_pages.platform_dashboard import (
    render as platform_dashboard_page
)
from app.ui_pages.error_dashboard import (
    render as error_dashboard_page
)
from app.ui_pages.audit_dashboard import (
    render as audit_dashboard_page
)

from app.ui_pages.agent_catalog import render as agent_catalog_page
from app.ui_pages.agent_runner import render as agent_runner_page

from app.ui_pages.workflow_monitor import (
    render as workflow_monitor_page
)
from app.ui_pages.workflow_compare import (
    render as workflow_compare_page
)
from app.ui_pages.workflow_builder import render as workflow_builder_page
from app.ui_pages.workflow_visualizer import render as workflow_visualizer_page
from app.ui_pages.workflow_library import render as workflow_library_page
from app.ui_pages.workspaces import (
    render as workspaces_page
)

from app.ui_pages.workflow_marketplace import render as workflow_marketplace_page
from app.ui_pages.workflow_import import render as workflow_import_page
from app.ui_pages.save_template import render as save_template_page

from app.ui_pages.workflow_executor import render as workflow_executor_page
from app.ui_pages.workflow_execution_history import render as workflow_execution_history_page
from app.ui_pages.workflow_replay import render as workflow_replay_page
from app.ui_pages.workflow_versions import (
    render as workflow_versions_page
)

from app.ui_pages.workflow_generator import render as workflow_generator_page
from app.ui_pages.workflow_analytics import render as workflow_analytics_page
from app.ui_pages.dag_visualizer import render as dag_visualizer_page

from app.ui_pages.approval_analytics import (
    render as approval_analytics_page
)

from app.ui_pages.approval_escalation_dashboard import (
    render as approval_escalation_dashboard_page
)

from app.ui_pages.approval_center import render as approval_center_page
from app.ui_pages.workflow_scheduler import render as workflow_scheduler_page
from app.ui_pages.scheduler_control import (
    render as scheduler_control_page
)

from app.ui_pages.execution_center import render as execution_center_page
from app.ui_pages.execution_history import render as execution_history_page
from app.ui_pages.execution_search import render as execution_search_page
from app.ui_pages.log_viewer import render as log_viewer_page

from app.ui_pages.memory import render as memory_page
from app.ui_pages.metrics import render as metrics_page

from app.ui_pages.notification_center import (
    render as notification_center_page
)
from app.ui_pages.resume_debug import (
    render as resume_debug_page
)

from app.ui_pages.system_health import (
    render as system_health_page
)

from app.ui_pages.profile import render as profile_page
from app.ui_pages.api_vault import render as api_vault_page
from app.ui_pages.settings import render as settings_page
from app.ui_pages.contact import render as contact_page

from app.ui_pages.database_dashboard import render as database_dashboard_page
from app.ui_pages.test_current_user_service import render as test_current_user_service_page

st.set_page_config(
    page_title="AgentForge OS",
    page_icon="🚀",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    auth_page()
    st.stop()

user = st.session_state.get("user")

if user:
    try:
        if isinstance(user, dict):
            st.sidebar.success(f"👤 {user.get('email', 'Unknown User')}")
        else:
            st.sidebar.success(f"👤 {user.email}")
    except Exception:
        st.sidebar.success("👤 Logged In")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

NAVIGATION_OPTIONS = {
    "📊 Dashboards": [
        "Dashboard", "Platform Dashboard", "Error Dashboard", "Audit Dashboard", "System Health"
    ],
    "⚙️ Workflow Management": [
        "Workflow Monitor", "Workflow Builder", "Workflow Visualizer", "Workflow Library",
        "Workspaces", "Workflow Marketplace", "Workflow Import", "Save Template",
        "Workflow Executor", "Workflow Execution History", "Workflow Replay",
        "Workflow Versions", "Workflow Analytics", "DAG Visualizer", "AI Workflow Generator",
        "Workflow Compare"
    ],
    "✅ Approvals & Scheduling": [
        "Approval Center", "Approval Intelligence", "Approval Escalation Dashboard",
        "Workflow Scheduler", "Scheduler Control"
    ],
    "🤖 Agent & Execution": [
        "Agent Catalog", "Agent Runner", "Execution Center", "Execution History",
        "Execution Search", "Log Viewer"
    ],
    "Data & Monitoring": [
        "Memory", "Metrics", "Database Dashboard"
    ],
    "🛠️ Developer Tools": [
        "Resume Debug", "Notification Center"
    ],
    "User & System": [
        "Profile", "API Vault", "Settings", "Contact"
    ],
    "Test Services": [
        "Test Current User Service"
    ]
}

def set_page_from_sidebar_radio(group_key):
    st.session_state.current_page = st.session_state[group_key]

with st.sidebar:
    st.markdown("## Navigation")
    for group_name, pages in NAVIGATION_OPTIONS.items():
        clean_group_name = "".join(char for char in group_name if char.isalnum())
        radio_key = f"radio_{clean_group_name}"
        is_expanded = any(st.session_state.current_page == page for page in pages)
        try:
            current_selection_index = pages.index(st.session_state.current_page)
        except ValueError:
            current_selection_index = 0
        with st.expander(group_name, expanded=is_expanded):
            st.radio(
                "Select a page",
                options=pages,
                index=current_selection_index,
                key=radio_key,
                on_change=set_page_from_sidebar_radio,
                args=(radio_key,)
            )

orchestrator = st.session_state.get("orchestrator")
stored_workflows = st.session_state.get("stored_workflows", {})
menu = st.session_state.current_page

if menu == "Dashboard":
    dashboard_page(orchestrator, stored_workflows)
elif menu == "Platform Dashboard":
    platform_dashboard_page()
elif menu == "Error Dashboard":
    error_dashboard_page()
elif menu == "Audit Dashboard":
    audit_dashboard_page()
elif menu == "System Health":
    system_health_page()
elif menu == "Agent Catalog":
    agent_catalog_page()
elif menu == "Agent Runner":
    agent_runner_page(orchestrator)
elif menu == "Workflow Monitor":
    workflow_monitor_page()
elif menu == "Workflow Compare":
    workflow_compare_page()
elif menu == "Workflow Builder":
    workflow_builder_page()
elif menu == "Workflow Visualizer":
    workflow_visualizer_page(stored_workflows)
elif menu == "Workflow Library":
    workflow_library_page()
elif menu == "Workspaces":
    workspaces_page()
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
elif menu == "Workflow Versions":
    workflow_versions_page()
elif menu == "Workflow Analytics":
    workflow_analytics_page()
elif menu == "DAG Visualizer":
    dag_visualizer_page()
elif menu == "Approval Intelligence":
    approval_analytics_page()
elif menu == "Approval Escalation Dashboard":
    approval_escalation_dashboard_page()
elif menu == "Approval Center":
    approval_center_page()
elif menu == "Workflow Scheduler":
    workflow_scheduler_page()
elif menu == "Scheduler Control":
    scheduler_control_page()
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
    memory_page(orchestrator)
elif menu == "Metrics":
    metrics_page(orchestrator)
elif menu == "Database Dashboard":
    database_dashboard_page()
elif menu == "Notification Center":
    notification_center_page()
elif menu == "Resume Debug":
    resume_debug_page()
elif menu == "Profile":
    profile_page()
elif menu == "API Vault":
    api_vault_page()
elif menu == "Settings":
    settings_page()
elif menu == "Contact":
    contact_page()
elif menu == "Test Current User Service":
    test_current_user_service_page()
