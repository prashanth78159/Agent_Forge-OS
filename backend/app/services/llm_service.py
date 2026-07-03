
from groq import Groq
from openai import OpenAI
from anthropic import Anthropic
from google import genai


class LLMService:

    AVAILABLE_MODELS = {

        "Groq": [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile"
        ],

        "OpenAI": [
            "gpt-4o",
            "gpt-4o-mini"
        ],

        "Anthropic": [
            "claude-3-5-haiku-latest",
            "claude-3-5-sonnet-latest"
        ],

        "Gemini": [
            "gemini-2.5-flash",
            "gemini-2.5-pro"
        ],

        "Deepseek": [
            "deepseek-chat"
        ],

        "OpenRouter": [
            "openai/gpt-4o-mini",
            "anthropic/claude-3.5-haiku"
        ]
    }

    TOKENS_PER_WORD = 1.5

    def __init__(
        self,
        llm_provider,
        api_key,
        model_name
    ):

        self.llm_provider = llm_provider
        self.model_name = model_name

        if not api_key:

            raise ValueError(
                f"API key missing for {llm_provider}"
            )

        if llm_provider == "Groq":

            self.client = Groq(
                api_key=api_key
            )

        elif llm_provider == "OpenAI":

            self.client = OpenAI(
                api_key=api_key
            )

        elif llm_provider == "Anthropic":

            self.client = Anthropic(
                api_key=api_key
            )

        elif llm_provider == "Gemini":

            self.client = genai.Client(
                api_key=api_key
            )

        elif llm_provider == "Deepseek":

            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com/v1"
            )

        elif llm_provider == "OpenRouter":

            self.client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )

        else:

            raise ValueError(
                f"Unsupported provider: {llm_provider}"
            )

    def _estimate_tokens(
        self,
        text
    ):

        if not text:
            return 0

        return int(
            len(text.split())
            * self.TOKENS_PER_WORD
        )

    def _calculate_cost(
        self,
        prompt_tokens,
        completion_tokens
    ):

        return 0.0

    def generate(
        self,
        prompt,
        memory_context=""
    ):

        full_prompt = prompt

        if memory_context:

            full_prompt = (
                "Context:\n"
                + str(memory_context)
                + "\n\n"
                + str(prompt)
            )

        try:

            if self.llm_provider in [
                "Groq",
                "OpenAI",
                "Deepseek",
                "OpenRouter"
            ]:

                response = (
                    self.client
                    .chat
                    .completions
                    .create(
                        model=self.model_name,
                        messages=[
                            {
                                "role": "user",
                                "content": full_prompt
                            }
                        ]
                    )
                )

                output = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                prompt_tokens = 0
                completion_tokens = 0

                if (
                    hasattr(response, "usage")
                    and response.usage
                ):

                    prompt_tokens = (
                        response.usage.prompt_tokens
                    )

                    completion_tokens = (
                        response.usage.completion_tokens
                    )

            elif self.llm_provider == "Anthropic":

                response = (
                    self.client.messages.create(
                        model=self.model_name,
                        max_tokens=2000,
                        messages=[
                            {
                                "role": "user",
                                "content": full_prompt
                            }
                        ]
                    )
                )

                output = (
                    response.content[0].text
                )

                prompt_tokens = (
                    self._estimate_tokens(
                        full_prompt
                    )
                )

                completion_tokens = (
                    self._estimate_tokens(
                        output
                    )
                )

            elif self.llm_provider == "Gemini":

                response = (
                    self.client
                    .models
                    .generate_content(
                        model=self.model_name,
                        contents=full_prompt
                    )
                )

                output = response.text

                prompt_tokens = (
                    self._estimate_tokens(
                        full_prompt
                    )
                )

                completion_tokens = (
                    self._estimate_tokens(
                        output
                    )
                )

            else:

                raise ValueError(
                    f"Unsupported provider: {self.llm_provider}"
                )

            total_cost = (
                self._calculate_cost(
                    prompt_tokens,
                    completion_tokens
                )
            )

            return (
                output,
                prompt_tokens,
                completion_tokens,
                total_cost
            )

        except Exception as e:

            print("\n" + "=" * 80)
            print("LLM ERROR")
            print(type(e))
            print(str(e))
            print("=" * 80 + "\n")

            raise

    @classmethod
    def get_available_models(
        cls
    ):

        return cls.AVAILABLE_MODELS

    @classmethod
    def get_default_model(
        cls,
        provider
    ):

        models = (
            cls.AVAILABLE_MODELS
            .get(
                provider,
                []
            )
        )

        return (
            models[0]
            if models
            else None
        )
