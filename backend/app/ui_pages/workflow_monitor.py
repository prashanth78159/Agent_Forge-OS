
import pandas as pd
import streamlit as st

from app.config.database import db


def render():

    st.title(
        "📡 Workflow Monitor"
    )

    executions = (

        db.client

        .table(
            "workflow_executions"
        )

        .select("*")

        .order(
            "created_at",
            desc=True
        )

        .execute()

    )

    rows = executions.data

    if not rows:

        st.info(
            "No workflow executions found."
        )

        return

    df = pd.DataFrame(
        rows
    )

    latest = rows[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Latest Status",
        latest.get(
            "status",
            "Unknown"
        )
    )

    c2.metric(
        "Progress %",
        latest.get(
            "progress",
            0
        )
    )

    c3.metric(
        "Total Executions",
        len(rows)
    )

    running = len(
        [
            r
            for r in rows
            if r.get("status")
            ==
            "RUNNING"
        ]
    )

    c4.metric(
        "Running",
        running
    )

    st.subheader(
        "Recent Executions"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    execution_options = [

        f"{r['id']} | {r.get('status','')}"

        for r in rows

    ]

    selected = st.selectbox(
        "Inspect Execution",
        execution_options
    )

    execution_id = (
        selected.split(
            " | "
        )[0]
    )

    node_result = (

        db.client

        .table(
            "workflow_node_status"
        )

        .select("*")

        .eq(
            "execution_id",
            execution_id
        )

        .execute()

    )

    node_rows = (
        node_result.data
    )

    st.subheader(
        "Node Status"
    )

    if node_rows:

        node_df = pd.DataFrame(
            node_rows
        )

        st.dataframe(
            node_df,
            use_container_width=True
        )

    else:

        st.info(
            "No node statuses found."
        )

    try:

        output_result = (

            db.client

            .table(
                "workflow_node_outputs"
            )

            .select("*")

            .eq(
                "workflow_execution_id",
                execution_id
            )

            .execute()

        )

        outputs = (
            output_result.data
        )

        st.subheader(
            "Node Outputs"
        )

        if outputs:

            output_df = pd.DataFrame(
                outputs
            )

            st.dataframe(
                output_df,
                use_container_width=True
            )

        else:

            st.info(
                "No outputs found."
            )

    except Exception as e:

        st.warning(
            str(e)
        )

    st.button(
        "🔄 Refresh"
    )
