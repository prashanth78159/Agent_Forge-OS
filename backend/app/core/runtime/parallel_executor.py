
from concurrent.futures import (
    ThreadPoolExecutor
)


class ParallelExecutor:

    @staticmethod
    def execute(
        fn,
        tasks
    ):

        results = []

        with ThreadPoolExecutor(
            max_workers=4
        ) as executor:

            futures = [

                executor.submit(
                    fn,
                    task
                )

                for task in tasks

            ]

            for future in futures:

                results.append(
                    future.result()
                )

        return results
