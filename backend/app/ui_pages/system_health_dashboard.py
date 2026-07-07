
import streamlit as st
import psutil
import time

def render():

    st.title(
        "🏥 System Health Dashboard"
    )

    st.write(
        "Monitoring real-time system health metrics."
    )

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

    while True:
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
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

        # Update history for charts
        cpu_history.append(cpu_percent)
        if len(cpu_history) > 20: # Keep last 20 readings
            cpu_history.pop(0)
        cpu_chart.add_rows(cpu_history[-1:])

        memory_history.append(memory_percent)
        if len(memory_history) > 20: # Keep last 20 readings
            memory_history.pop(0)
        memory_chart.add_rows(memory_history[-1:])

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

        time.sleep(2) # Refresh every 2 seconds
        st.experimental_rerun() # Rerun the script to update Streamlit components
