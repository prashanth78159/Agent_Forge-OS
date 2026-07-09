
import streamlit as st
import pandas as pd
from datetime import datetime
import psutil
import time

from app.config.database import db
from app.services.health_check_service import HealthCheckService

def render():
    st.title("🏥 System Health Dashboard")

    st.markdown("--- This dashboard provides a snapshot of the application's core service health. ---")

    if st.button("Run Health Scan"): # Button to trigger checks
        st.success("Running health scan...")
        st.experimental_rerun() # Rerun to refresh all data

    st.header("1. Core Service Health")

    # Database Connection Check
    db_connected, db_status_msg = HealthCheckService.check_database_connection()
    st.markdown(f"Database Connectivity: **{'✅ Healthy' if db_connected else '❌ Unhealthy'}** ({db_status_msg})")

    # Check table accessibility for key tables
    st.subheader("Database Table Accessibility")
    tables_to_check = [
        "workflows", "workflow_executions", "workflow_approvals",
        "workflow_resume_queue", "workflow_node_outputs",
        "notifications", "workflow_execution_snapshot"
    ]
    for table_name in tables_to_check:
        accessible, msg = HealthCheckService.check_table_accessibility(table_name)
        st.markdown(f"- Table `{table_name}`: **{'✅ Accessible' if accessible else '❌ Inaccessible'}** ({msg})")


    st.header("2. Workflow & Approval Status")

    # Recent Workflow Executions
    st.subheader("Recent Workflow Executions")
    recent_executions = HealthCheckService.get_recent_workflow_executions(limit=10)
    if recent_executions:
        df_executions = pd.DataFrame(recent_executions)
        st.dataframe(df_executions, use_container_width=True)
    else:
        st.info("No recent workflow executions found.")

    # Pending Approvals Count
    pending_approvals_count = HealthCheckService.get_pending_approvals_count()
    st.metric(label="Pending Approvals in Queue", value=pending_approvals_count)

    # Resume Engine Status
    resume_engine_status = HealthCheckService.get_resume_engine_status()
    st.metric(label="Resume Engine Status", value=resume_engine_status)

    st.header("3. System Resource Usage")
    # Create placeholders for live updates
    cpu_metric = st.empty()
    memory_metric = st.empty()
    disk_metric = st.empty()
    network_metric = st.empty()
    alerts_container = st.empty()

    st.subheader("CPU Usage History")
    cpu_chart = st.line_chart([])

    st.subheader("Memory Usage History")
    memory_chart = st.line_chart([])

    cpu_history = []
    memory_history = []

    # While True loop commented out for direct Streamlit rerun compatibility
    # Streamlit reruns the whole script on interaction/changes, 
    # so a continuous loop here would block. Metrics update on each rerun.
    
    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_metric.metric(label="CPU Usage", value=f"{cpu_percent:.1f}%", delta=None)

    # Memory Usage
    svmem = psutil.virtual_memory()
    memory_percent = svmem.percent
    memory_metric.metric(label="Memory Usage", value=f"{memory_percent:.1f}%", delta=None)

    # Disk Usage
    disk_usage = psutil.disk_usage('/')
    disk_percent = disk_usage.percent
    disk_metric.metric(label="Disk Usage", value=f"{disk_percent:.1f}%", delta=None)

    # Network I/O
    net_io = psutil.net_io_counters()
    network_metric.metric("Network I/O (Sent/Recv)", f"{net_io.bytes_sent / (1024*1024):.2f}MB / {net_io.bytes_recv / (1024*1024):.2f}MB", delta=None)

    # For simplicity, historical data in Streamlit charts should ideally be managed outside the render function
    # or loaded from session_state for persistence across reruns.
    # For this demonstration, we'll just show current values.
    # Updating history directly in a render function without session state or external storage is tricky.
    
    # Simple Alerts
    alerts = []
    if cpu_percent > 80:
        alerts.append("⚠️ High CPU Usage!")
    if memory_percent > 80:
        alerts.append("⚠️ High Memory Usage!")
    if disk_percent > 90:
        alerts.append("🚨 Critical Disk Usage!")

    if alerts:
        with alerts_container.container():
            for alert in alerts:
                st.warning(alert)
    else:
        alerts_container.empty()

    st.markdown(f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_ (System metrics update on page refresh)")
