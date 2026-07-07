

import streamlit as st

from datetime import (
    datetime,
    timezone,
    date
)

import pandas as pd

from app.config.database import db


def render():

    st.title(
        "📊 Approval Intelligence Dashboard"
    )

    rows = (
        db.client
        .table(
            "workflow_approvals"
        )
        .select("*")
        .execute()
        .data
    )

    # ---------------------------
    # Filters
    # ---------------------------

    st.subheader(
        "Filters"
    )

    col1, col2 = st.columns(2)

    status_filter = col1.selectbox(
        "Status",
        [
            "ALL",
            "PENDING",
            "APPROVED",
            "REJECTED"
        ]
    )

    show_overdue_only = col2.checkbox(
        "Show Overdue Only"
    )

    col3, col4 = st.columns(2)

    execution_filter = col3.text_input(
        "Execution ID Contains"
    )

    node_filter = col4.text_input(
        "Node ID Contains"
    )

    col5, col6 = st.columns(2)

    start_date = col5.date_input(
        "Start Date",
        value=date(2025, 1, 1)
    )

    end_date = col6.date_input(
        "End Date",
        value=date.today()
    )

    col7, col8 = st.columns(2)

    group_filter = col7.selectbox(
        "Approver Group",
        [
            "ALL",
            "Manager",
            "Director",
            "Finance"
        ]
    )

    filtered_rows = rows.copy()

    # ---------------------------
    # Status Filter
    # ---------------------------

    if status_filter != "ALL":

        filtered_rows = [
            r
            for r in filtered_rows
            if r.get("status") == status_filter
        ]

    # ---------------------------
    # Execution ID Filter
    # ---------------------------

    if execution_filter:

        filtered_rows = [
            r
            for r in filtered_rows
            if execution_filter.lower()
            in str(
                r.get(
                    "execution_id",
                    ""
                )
            ).lower()
        ]

    # ---------------------------
    # Node ID Filter
    # ---------------------------

    if node_filter:

        filtered_rows = [
            r
            for r in filtered_rows
            if node_filter.lower()
            in str(
                r.get(
                    "node_id",
                    ""
                )
            ).lower()
        ]

    # ---------------------------
    # Date Filter
    # ---------------------------

    date_filtered = []

    for row in filtered_rows:

        created_at = row.get(
            "created_at"
        )

        if not created_at:
            continue

        try:

            created_date = (
                datetime
                .fromisoformat(
                    created_at.replace(
                        "Z",
                        "+00:00"
                    )
                )
                .date()
            )

            if (
                start_date
                <= created_date
                <= end_date
            ):

                date_filtered.append(
                    row
                )

        except Exception:

            pass

    filtered_rows = date_filtered

    # ---------------------------
    # Group Filter
    # ---------------------------

    if group_filter != "ALL":

        filtered_rows = [
            r
            for r in filtered_rows
            if r.get(
                "approver_group"
            )
            ==
            group_filter
        ]

    # ---------------------------
    # Overdue Detection
    # ---------------------------

    overdue = []

    now = datetime.now(
        timezone.utc
    )

    for row in filtered_rows:

        if (
            row.get("status")
            == "PENDING"
            and row.get("due_at")
        ):

            try:

                due = datetime.fromisoformat(
                    row["due_at"]
                )

                if due < now:

                    overdue.append(
                        row
                    )

            except Exception:

                pass

    if show_overdue_only:

        filtered_rows = overdue

    # ---------------------------
    # Metrics
    # ---------------------------

    total = len(
        filtered_rows
    )

    approved = len([
        r
        for r in filtered_rows
        if r.get("status")
        == "APPROVED"
    ])

    rejected = len([
        r
        for r in filtered_rows
        if r.get("status")
        == "REJECTED"
    ])

    pending = len([
        r
        for r in filtered_rows
        if r.get("status")
        == "PENDING"
    ])

    escalated = len([
        r
        for r in filtered_rows
        if r.get("escalated") == True
    ])

    approval_rate = 0
    rejection_rate = 0

    if total > 0:

        approval_rate = round(
            approved * 100 / total,
            2
        )

        rejection_rate = round(
            rejected * 100 / total,
            2
        )

    # ---------------------------
    # Average Approval Time
    # ---------------------------

    approval_times = []

    for row in filtered_rows:

        if (
            row.get("created_at")
            and row.get("approved_at")
        ):

            try:

                created = datetime.fromisoformat(
                    row["created_at"].replace(
                        "Z",
                        "+00:00"
                    )
                )

                approved_time = datetime.fromisoformat(
                    row["approved_at"].replace(
                        "Z",
                        "+00:00"
                    )
                )

                hours = (
                    approved_time
                    - created
                ).total_seconds() / 3600

                approval_times.append(
                    hours
                )

            except Exception:

                pass

    avg_approval_time = (
        round(
            sum(
                approval_times
            ) / len(
                approval_times
            ),
            2
        )
        if approval_times
        else 0
    )

    # ---------------------------
    # KPI Cards
    # ---------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Approvals",
        total
    )

    c2.metric(
        "Approved",
        approved
    )

    c3.metric(
        "Rejected",
        rejected
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Pending",
        pending
    )

    c5.metric(
        "Overdue",
        len(overdue)
    )

    c6.metric(
        "Approval Rate %",
        approval_rate
    )

    st.metric(
        "Rejection Rate %",
        rejection_rate
    )

    st.metric(
        "Avg Approval Time (Hours)",
        avg_approval_time
    )

    st.metric(
        "Escalated",
        escalated
    )

    level1 = len([
        r
        for r in filtered_rows
        if r.get(
            "approval_level"
        ) == 1
    ])

    level2 = len([
        r
        for r in filtered_rows
        if r.get(
            "approval_level"
        ) == 2
    ])

    level3 = len([
        r
        for r in filtered_rows
        if r.get(
            "approval_level"
        ) == 3
    ])

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Manager Approvals",
        level1
    )

    c2.metric(
        "Director Approvals",
        level2
    )

    c3.metric(
        "Finance Approvals",
        level3
    )

    # ---------------------------
    # Status Chart
    # ---------------------------

    st.divider()

    st.subheader(
        "Approval Status Distribution"
    )

    chart_df = pd.DataFrame(
        {
            "Status": [
                "Approved",
                "Rejected",
                "Pending"
            ],
            "Count": [
                approved,
                rejected,
                pending
            ]
        }
    )

    st.bar_chart(
        chart_df.set_index(
            "Status"
        )
    )

    # ---------------------------
    # Trend Chart
    # ---------------------------

    trend = {}

    for row in filtered_rows:

        created = row.get(
            "created_at"
        )

        if created:

            day = created[:10]

            trend[day] = (
                trend.get(
                    day,
                    0
                )
                + 1
            )

    if trend:

        trend_df = pd.DataFrame(
            {
                "Date": list(
                    trend.keys()
                ),
                "Approvals": list(
                    trend.values()
                )
            }
        )

        st.divider()

        st.subheader(
            "Approval Trend"
        )

        st.line_chart(
            trend_df.set_index(
                "Date"
            )
        )

    # ---------------------------
    # Overdue Table
    # ---------------------------

    st.divider()

    st.subheader(
        "🚨 Overdue Approval Requests"
    )

    if overdue:

        st.dataframe(
            overdue,
            use_container_width=True
        )

    else:

        st.success(
            "No overdue approvals."
        )

    # ---------------------------
    # Records
    # ---------------------------

    st.divider()

    st.subheader(
        "📋 Approval Records"
    )

    st.dataframe(
        filtered_rows,
        use_container_width=True
    )
