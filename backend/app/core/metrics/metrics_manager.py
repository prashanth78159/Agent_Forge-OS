
import time

class MetricsManager:

    def __init__(self):

        self.execution_metrics = {}
        self.current_execution_id = None

    def start_execution(
        self,
        execution_id
    ):

        self.current_execution_id = (
            execution_id
        )

        self.execution_metrics[
            execution_id
        ] = []

    def log_step_metrics(
        self,
        step_name,
        llm_response_content,
        prompt_tokens,
        completion_tokens,
        total_cost,
        duration
    ):

        if not self.current_execution_id:
            return

        self.execution_metrics[
            self.current_execution_id
        ].append({

            "timestamp":
                time.time(),

            "step_name":
                step_name,

            "prompt_tokens":
                prompt_tokens,

            "completion_tokens":
                completion_tokens,

            "total_tokens":
                prompt_tokens
                + completion_tokens,

            "total_cost":
                total_cost,

            "duration":
                duration
        })

    def get_all_executions_metrics(
        self
    ):

        return self.execution_metrics
