
import os
import streamlit as st


def render():

    st.title(
        "🏢 Platform Health Dashboard"
    )

    ui_pages = [
        "workflow_builder.py",
        "workflow_executor.py",
        "workflow_replay.py",
        "workflow_generator.py",
        "workflow_analytics.py",
        "workflow_scheduler.py",
        "dag_visualizer.py",
        "approval_center.py",
        "api_vault.py",
        "profile.py",
        "settings.py"
    ]

    base = (
        "/content/Agent_Forge-OS/"
        "backend/app/ui_pages"
    )

    rows = []

    for page in ui_pages:

        path = os.path.join(
            base,
            page
        )

        if not os.path.exists(path):

            rows.append(
                {
                    "Page": page,
                    "Status": "❌ Missing",
                    "Lines": 0
                }
            )

            continue

        with open(
            path,
            "r"
        ) as fp:

            lines = len(
                fp.readlines()
            )

        if lines < 20:

            status = "⚠ Placeholder"

        elif lines < 100:

            status = "🟡 Partial"

        else:

            status = "✅ Implemented"

        rows.append(
            {
                "Page": page,
                "Status": status,
                "Lines": lines
            }
        )

    st.dataframe(
        rows,
        use_container_width=True
    )

    implemented = len(
        [
            r
            for r in rows
            if r["Status"] == "✅ Implemented"
        ]
    )

    partial = len(
        [
            r
            for r in rows
            if r["Status"] == "🟡 Partial"
        ]
    )

    placeholder = len(
        [
            r
            for r in rows
            if r["Status"] == "⚠ Placeholder"
        ]
    )

    missing = len(
        [
            r
            for r in rows
            if r["Status"] == "❌ Missing"
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Implemented",
        implemented
    )

    c2.metric(
        "Partial",
        partial
    )

    c3.metric(
        "Placeholder",
        placeholder
    )

    c4.metric(
        "Missing",
        missing
    )
