
import streamlit as st
import pandas as pd
import plotly.express as px

def render(orchestrator):

    st.title("📈 Metrics")

    if not orchestrator:
        return

    metrics = (
        orchestrator
        .metrics_manager
        .get_all_executions_metrics()
    )

    rows = []

    for execution_id, items in metrics.items():

        for item in items:

            rows.append({

                "Execution":
                    execution_id,

                "Step":
                    item.get(
                        "step_name"
                    ),

                "Tokens":
                    item.get(
                        "total_tokens"
                    ),

                "Cost":
                    item.get(
                        "total_cost"
                    ),

                "Duration":
                    item.get(
                        "duration"
                    )
            })

    if not rows:

        st.info(
            "No metrics yet"
        )

        return

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True
    )

    fig = px.bar(
        df,
        x="Step",
        y="Tokens",
        color="Execution",
        title="Token Usage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
