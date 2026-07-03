
class ApprovalService:

    @staticmethod
    def requires_approval(
        node
    ):

        return (
            node.get(
                "requires_approval",
                False
            )
        )
