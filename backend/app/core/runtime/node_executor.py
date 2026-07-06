
class NodeExecutor:

    @staticmethod
    def get_retry_count(
        node
    ):

        return node.get(
            "retries",
            3
        )
