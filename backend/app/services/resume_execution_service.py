
from app.config.database import db

from app.services.execution_snapshot_service import (
    ExecutionSnapshotService
)

from app.services.resume_dag_service import (
    ResumeDAGService
)

from app.services.resume_node_executor import (
    ResumeNodeExecutor
)

from app.services.audit_service import (
    AuditService
)


class ResumeExecutionService:

    @staticmethod
    def resume_execution(
        execution_id
    ):

        snapshot = (
            ExecutionSnapshotService
            .get_snapshot(
                execution_id
            )
        )

        if not snapshot:

            return {
                "success": False
            }

        outputs = dict(
            snapshot.get(
                "outputs",
                {}
            )
        )

        completed_nodes = list(
            snapshot.get(
                "completed_nodes",
                []
            )
        )

        remaining_nodes = (
            ResumeDAGService
            .get_remaining_nodes(
                execution_id
            )
        )

        for node in remaining_nodes:

            output = (
                ResumeNodeExecutor
                .execute_node(
                    execution_id,
                    node,
                    outputs
                )
            )

            outputs[
                node["id"]
            ] = output

            completed_nodes.append(
                node["id"]
            )

        ExecutionSnapshotService.save_snapshot(

            execution_id,

            snapshot["workflow_json"],

            outputs,

            completed_nodes

        )

        db.client.table(
            "workflow_executions"
        ).update(
            {
                "status":
                    "COMPLETED",

                "progress":
                    100
            }
        ).eq(
            "id",
            execution_id
        ).execute()

        AuditService.log_event(

            execution_id,

            "RESUME",

            "Workflow fully resumed"

        )

        return {

            "success":
                True,

            "completed_nodes":
                completed_nodes,

            "outputs":
                outputs

        }
