
import json
import streamlit as st

from app.services.settings_service import (
    SettingsService
)

from app.services.llm_service import (
    LLMService
)

from app.services.workflow_service import (
    WorkflowService
)


def get_provider_key(provider):

    mapping = {

        "Groq":
            "groq_api_key",

        "OpenAI":
            "openai_api_key",

        "Anthropic":
            "anthropic_api_key",

        "Gemini":
            "gemini_api_key",

        "Deepseek":
            "deepseek_api_key",

        "OpenRouter":
            "openrouter_api_key"
    }

    return SettingsService.get_setting(
        mapping.get(provider)
    )


def render():

    st.title(
        "🤖 AI Workflow Generator"
    )

    idea = st.text_area(
        "Describe Workflow",
        height=150
    )

    if st.button(
        "Generate Workflow"
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

        api_key = (
            get_provider_key(
                provider
            )
        )

        llm = LLMService(
            provider,
            api_key,
            model
        )

        prompt = f'''
        You are an AI Workflow Architect.

        Generate ONLY JSON.

        Output format:

        {{
          "nodes": [
            {{
              "id":"planner",
              "prompt":"..."
            }}
          ],
          "edges":[
            {{
              "source":"planner",
              "target":"writer"
            }}
          ]
        }}

        Workflow Request:

        {idea}
        '''

        (
            output,
            prompt_tokens,
            completion_tokens,
            total_cost
        ) = llm.generate(
            prompt
        )

        st.code(
            output,
            language="json"
        )

        try:

            workflow_json = (
                json.loads(
                    output
                )
            )

            workflow_name = (
                st.text_input(
                    "Workflow Name",
                    "AI Generated Workflow"
                )
            )

            if st.button(
                "Save Workflow"
            ):

                WorkflowService.save_workflow(
                    workflow_name,
                    workflow_json
                )

                st.success(
                    "Workflow Saved"
                )

        except Exception:

            st.warning(
                "Generated output wasn't valid JSON."
            )
