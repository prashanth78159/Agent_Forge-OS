
import json
import streamlit as st

from app.services.template_service import (
    TemplateService
)

from app.services.workflow_service import (
    WorkflowService
)


def render():

    st.title(
        "🛒 Workflow Marketplace"
    )

    templates = (
        TemplateService
        .get_templates()
    )

    if not templates:

        st.info(
            "No templates available."
        )

        return

    for template in templates:

        with st.expander(
            template["name"]
        ):

            st.write(
                template.get(
                    "description",
                    ""
                )
            )

            workflow_json = (
                template.get(
                    "workflow_json",
                    {}
                )
            )

            st.code(
                json.dumps(
                    workflow_json,
                    indent=2
                )
            )

            if st.button(
                f"Clone-{template['id']}"
            ):

                WorkflowService.save_workflow(
                    f"Copy - {template['name']}",
                    workflow_json
                )

                st.success(
                    "Workflow cloned"
                )

            st.download_button(

                label="Export JSON",

                data=json.dumps(
                    workflow_json,
                    indent=2
                ),

                file_name=
                    f"{template['name']}.json",

                mime=
                    "application/json"
            )
