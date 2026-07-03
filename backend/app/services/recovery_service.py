
class RecoveryService:

    @staticmethod
    def retry_failed_node(
        execution_id,
        node_name
    ):

        print(
            f"Retrying {node_name}"
        )

        return True
