
MODELS = {

    "OPENAI": [
        "gpt-4o",
        "gpt-4.1",
        "gpt-5"
    ],

    "ANTHROPIC": [
        "claude-opus",
        "claude-sonnet"
    ],

    "GEMINI": [
        "gemini-2.5-pro",
        "gemini-2.5-flash"
    ],

    "GROQ": [
        "llama-3"
    ],

    "DEEPSEEK": [
        "deepseek-chat"
    ]
}


class ModelRegistry:

    @staticmethod
    def get_models(provider):

        return MODELS.get(
            provider.upper(),
            []
        )

    @staticmethod
    def get_all():

        return MODELS
