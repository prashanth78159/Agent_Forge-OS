
from app.services.llm_service import LLMService


class BaseAgent:

    def __init__(
        self,
        name,
        llm_service,
        metrics_manager=None
    ):

        self.name = name
        self.llm_service = llm_service
        self.metrics_manager = metrics_manager

    def run(
        self,
        input_text,
        context
    ):

        raise NotImplementedError

    def _generate_and_log(
        self,
        prompt,
        memory_context=""
    ):

        import time

        start_time = time.time()

        response, prompt_tokens, completion_tokens, total_cost = (
            self.llm_service.generate(
                prompt,
                memory_context
            )
        )

        duration = (
            time.time() - start_time
        )

        if self.metrics_manager:

            self.metrics_manager.log_step_metrics(
                step_name=self.name,
                llm_response_content=response,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_cost=total_cost,
                duration=duration
            )

        return response
