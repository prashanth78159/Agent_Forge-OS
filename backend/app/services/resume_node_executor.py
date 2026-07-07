
from app.services.llm_service import (
    LLMService
)

from app.services.workflow_execution_service import (
    WorkflowExecutionService
)

from app.services.settings_service import (
    SettingsService
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


class ResumeNodeExecutor:

    @staticmethod
    def execute_node(
        execution_id,
        node,
        outputs
    ):

        prompt = node.get(
            "prompt",
            ""
        )

        context = "\n\n".join(
            str(v)
            for v in outputs.values()
        )

        final_prompt = (

            "Previous Workflow Context:\n\n"

            + context

            + "\n\nTask:\n\n"

            + prompt

        )

        provider = (
            SettingsService.get_setting(
                "provider"
            )
        )

        model = (
            SettingsService.get_setting(
                "model"
            )
        )

        api_key = get_provider_key(
            provider
        )

        llm = LLMService(

            provider,

            api_key,

            model

        )

        (
            output,
            _,
            _,
            _
        ) = llm.generate(
            final_prompt
        )

        WorkflowExecutionService.save_output(

            execution_id,

            node["id"],

            output

        )

        return output
