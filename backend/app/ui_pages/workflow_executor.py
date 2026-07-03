
import streamlit as st

from app.services.workflow_service import WorkflowService
from app.services.settings_service import SettingsService

from app.core.runtime.execution_engine import (
    ExecutionEngine
)


def get_provider_key(provider):

    mapping = {
        "Groq": "groq_api_key",
        "OpenAI": "openai_api_key",
        "Anthropic": "anthropic_api_key",
        "Gemini": "gemini_api_key",
        "Deepseek": "deepseek_api_key",
        "OpenRouter": "openrouter_api_key"
    }

    return SettingsService.get_setting(
        mapping.get(provider)
    )


def render():

    st.title(
        "⚙ Workflow Executor"
    )

    workflows = (
        WorkflowService.get_workflows()
    )

    if not workflows:

        st.warning(
            "No workflows found."
        )

        return

    names = [
        w["name"]
        for w in workflows
    ]

    workflow_name = st.selectbox(
        "Workflow",
        names
    )

    task = st.text_area(
        "Task",
        height=150
    )

    if st.button(
        "Run Workflow"
    ):

        provider = (
            SettingsService
            .get_setting(
                "provider"
            )
        )

        model = (
            SettingsService
            .get_setting(
                "model"
            )
        )

        api_key = get_provider_key(
            provider
        )

        workflow = next(
            w for w in workflows
            if w["name"] == workflow_name
        )

        progress = st.progress(0)

        progress.progress(20)

        engine = ExecutionEngine(
            provider,
            api_key,
            model
        )

        progress.progress(50)

        result = engine.run_workflow(
            workflow,
            task
        )

        progress.progress(100)

        st.success(
            result["execution_id"]
        )

        st.subheader(
            "Final Output"
        )

        st.write(
            result["final"]
        )
