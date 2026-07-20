
SUPPORTED_PROVIDERS = [

    "OPENAI",

    "ANTHROPIC",

    "GEMINI",

    "GROQ",

    "DEEPSEEK",

    "OPENROUTER"
]


class ProviderRegistry:

    @staticmethod
    def list_providers():

        return SUPPORTED_PROVIDERS
