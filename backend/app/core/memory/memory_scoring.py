
class MemoryScoring:

    @staticmethod
    def calculate_score(

        recency_score,

        frequency_score,

        feedback_score,

        success_score

    ):

        total = (

            recency_score

            + frequency_score

            + feedback_score

            + success_score

        )

        return min(total, 100)
