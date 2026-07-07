
from app.services.execution_snapshot_service import (
    ExecutionSnapshotService
)


class ResumeDAGService:

    @staticmethod
    def get_remaining_nodes(
        execution_id
    ):

        snapshot = (
            ExecutionSnapshotService
            .get_snapshot(
                execution_id
            )
        )

        if not snapshot:

            return []

        workflow_json = snapshot.get(
            "workflow_json",
            {}
        )

        completed_nodes = set(

            snapshot.get(
                "completed_nodes",
                []
            )

        )

        nodes = workflow_json.get(
            "nodes",
            []
        )

        remaining = []

        for node in nodes:

            node_id = node.get(
                "id"
            )

            if node_id not in completed_nodes:

                remaining.append(
                    node
                )

        return remaining
