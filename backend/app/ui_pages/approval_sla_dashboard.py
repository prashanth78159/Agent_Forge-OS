
import streamlit as st

from datetime import (
    datetime,
    timezone
)

from app.config.database import db


def render():

    st.title(
        "⏰ Approval SLA Dashboard"
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

    total = len(rows)

    approved = len([
        r for r in rows
        if r.get("status") == "APPROVED"
    ])

    rejected = len([
        r for r in rows
        if r.get("status") == "REJECTED"
    ])

    pending = len([
        r for r in rows
        if r.get("status") == "PENDING"
    ])

    overdue = []

    now = datetime.now(
        timezone.utc
    )

    for row in rows:

        if (
            row.get("status") == "PENDING"
            and
            row.get("due_at")
        ):

            due = datetime.fromisoformat(
                row["due_at"]
            )

            if due < now:

                overdue.append(
                    row
                )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total",
        total
    )

    col2.metric(
        "Pending",
        pending
    )

    col3.metric(
        "Approved",
        approved
    )

    col4.metric(
        "Rejected",
        rejected
    )

    col5.metric(
        "Overdue",
        len(overdue)
    )

    st.divider()

    st.subheader(
        "Overdue Approval Requests"
    )

    st.dataframe(
        overdue,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "All Approval Requests"
    )

    st.dataframe(
        rows,
        use_container_width=True
    )
