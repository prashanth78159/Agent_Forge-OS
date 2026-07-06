
import streamlit as st

from app.services.workflow_service import (
    WorkflowService
)

from app.services.schedule_service import (
    ScheduleService
)


def render():

    st.title(
        "⏰ Workflow Scheduler"
    )

    workflows = (
        WorkflowService.get_workflows()
    )

    if not workflows:

        st.warning(
            "No workflows available."
        )

        return

    workflow = st.selectbox(
        "Workflow",
        [w["name"] for w in workflows]
    )

    cron = st.text_input(
        "Cron Expression",
        "0 9 * * *"
    )

    if st.button(
        "Create Schedule"
    ):

        selected = next(
            w
            for w in workflows
            if w["name"] == workflow
        )

        ScheduleService.create_schedule(
            str(selected["id"]),
            cron
        )

        st.success(
            "Schedule Created"
        )

    st.subheader(
        "Existing Schedules"
    )

    st.write(
        ScheduleService.get_schedules()
    )
