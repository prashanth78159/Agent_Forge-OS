
import uuid
import streamlit as st

from app.core.agents.agent_orchestrator import AgentOrchestrator
from app.services.settings_service import SettingsService
from app.services.execution_service import ExecutionService


def get_provider_key(provider):

    mapping = {
        "Groq": "groq_api_key",
        "OpenAI": "openai_api_key",
        "Anthropic": "anthropic_api_key",
        "Gemini": "gemini_api_key",
        "Deepseek": "deepseek_api_key",
        "OpenRouter": "openrouter_api_key"
    }

    key_name = mapping.get(provider)

    if not key_name:
        return None

    return SettingsService.get_setting(key_name)


def render(orchestrator):

    st.title("🚀 Agent Runner")

    provider = SettingsService.get_setting("provider")
    model = SettingsService.get_setting("model")

    api_key = get_provider_key(provider)

    st.write(f"Provider: {provider}")
    st.write(f"Model: {model}")

    if not provider:
        st.warning("Configure Settings first.")
        return

    if not model:
        st.warning("Select a model first.")
        return

    if not api_key:
        st.warning(f"No API Key configured for {provider}")
        return

    task = st.text_area(
        "Task",
        height=200
    )

    if st.button("Run Agent"):

        if not task:
            st.warning("Enter a task.")
            return

        try:

            agent = AgentOrchestrator(
                llm_provider=provider,
                api_key=api_key,
                model_name=model
            )

            result = agent.run(task)

            execution_id = result.get(
                "execution_id",
                str(uuid.uuid4())
            )

            ExecutionService.save_execution(
                execution_id,
                "SUCCESS",
                result.get("final", "")
            )

            for log in result.get("logs", []):

                ExecutionService.save_log(
                    execution_id,
                    log.get("step", ""),
                    str(log.get("input", "")),
                    str(log.get("output", ""))
                )

            st.success(
                f"Execution Saved: {execution_id}"
            )

            st.subheader("Final Output")

            st.write(
                result.get("final", "")
            )

            with st.expander(
                "Execution Details"
            ):

                for log in result.get(
                    "logs",
                    []
                ):

                    st.markdown(
                        f"### {log.get('step')}"
                    )

                    st.code(
                        str(log.get("output"))
                    )

        except Exception as e:

            st.exception(e)
