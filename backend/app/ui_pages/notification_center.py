
import streamlit as st

from app.services.notification_service import (
    NotificationService
)


def render():

    st.title(
        "🔔 Notification Center"
    )

    rows = (
        NotificationService
        .get_notifications()
    )

    if not rows:

        st.info(
            "No notifications."
        )

        return

    for row in rows:

        with st.expander(
            row["title"]
        ):

            st.write(
                row["message"]
            )

            st.caption(
                row["created_at"]
            )
