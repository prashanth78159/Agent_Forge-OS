
import streamlit as st

from app.services.analytics_service import (
    AnalyticsService
)


def render():

    st.title(
        "📊 Platform Dashboard"
    )

    metrics = (
        AnalyticsService
        .get_metrics()
    )

    c1,c2 = st.columns(2)

    with c1:

        st.metric(
            "Workflows",
            metrics["workflows"]
        )

        st.metric(
            "Templates",
            metrics["templates"]
        )

    with c2:

        st.metric(
            "Agent Executions",
            metrics["executions"]
        )

        st.metric(
            "Workflow Runs",
            metrics["workflow_runs"]
        )
