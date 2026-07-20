
import time

from app.services.database_service import get_db


class PromptTestService:

    def __init__(self):

        self.db = get_db()

    def save_test_run(
        self,
        payload
    ):

        return (
            self.db.client
            .table("prompt_test_runs")
            .insert(payload)
            .execute()
        )

    def get_prompt_tests(
        self,
        prompt_id
    ):

        return (
            self.db.client
            .table("prompt_test_runs")
            .select("*")
            .eq("prompt_id", prompt_id)
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

    def calculate_latency(
        self,
        start_time
    ):

        return int(
            (time.time() - start_time)
            * 1000
        )
