
import pandas as pd
import streamlit as st

from app.config.database import db


def render():

    st.title(
        "📊 Workflow Analytics"
    )

    result = (
        db.client
        .table(
            "workflow_metrics"
        )
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    rows = result.data

    if not rows:

        st.info(
            "No workflow executions found."
        )

        return

    df = pd.DataFrame(rows)

    total_executions = len(df)

    total_prompt_tokens = int(
        df["prompt_tokens"].fillna(0).sum()
    )

    total_completion_tokens = int(
        df["completion_tokens"].fillna(0).sum()
    )

    total_cost = round(
        float(
            df["cost"].fillna(0).sum()
        ),
        4
    )

    avg_cost = round(
        float(
            df["cost"].fillna(0).mean()
        ),
        4
    )

    c1, c2 = st.columns(2)

    c3, c4 = st.columns(2)

    c1.metric(
        "Executions",
        total_executions
    )

    c2.metric(
        "Total Cost",
        f"${total_cost}"
    )

    c3.metric(
        "Prompt Tokens",
        total_prompt_tokens
    )

    c4.metric(
        "Completion Tokens",
        total_completion_tokens
    )

    st.metric(
        "Average Cost Per Workflow",
        f"${avg_cost}"
    )

    if "created_at" in df.columns:

        st.subheader(
            "Execution Trend"
        )

        trend = (
            df.groupby(
                "created_at"
            )
            .size()
        )

        st.line_chart(
            trend
        )

    st.subheader(
        "Workflow Metrics"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader(
        "Cost Distribution"
    )

    if "cost" in df.columns:

        st.bar_chart(
            df["cost"]
        )

    st.subheader(
        "Token Distribution"
    )

    token_df = pd.DataFrame(
        {
            "Prompt":
                df[
                    "prompt_tokens"
                ],

            "Completion":
                df[
                    "completion_tokens"
                ]
        }
    )

    st.bar_chart(
        token_df
    )
