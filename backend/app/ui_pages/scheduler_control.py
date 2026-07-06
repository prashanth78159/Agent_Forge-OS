
import streamlit as st

from app.services.scheduler_engine import (
    SchedulerEngine
)


def render():

    st.title(
        "⏰ Scheduler Control"
    )

    st.info(
        "Manual execution of all enabled schedules."
    )

    if st.button(
        "Run Scheduled Workflows"
    ):

        count = (
            SchedulerEngine
            .run_all_schedules()
        )

        st.success(
            f"{count} schedules executed."
        )
