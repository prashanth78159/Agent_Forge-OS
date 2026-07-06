
from app.config.database import db

from app.core.runtime.execution_engine import (
    ExecutionEngine
)

from app.services.workflow_service import (
    WorkflowService
)


class SchedulerEngine:

    @staticmethod
    def run_all_schedules():

        result = (
            db.client
            .table(
                "workflow_schedules"
            )
            .select("*")
            .eq(
                "enabled",
                True
            )
            .execute()
        )

        schedules = result.data

        executed = 0

        for schedule in schedules:

            workflow_id = (
                schedule["workflow_id"]
            )

            workflows = (
                WorkflowService
                .get_workflows()
            )

            workflow = next(

                (
                    w
                    for w in workflows
                    if str(w["id"])
                    ==
                    str(workflow_id)
                ),

                None

            )

            if not workflow:

                continue

            engine = ExecutionEngine(

                provider="groq",

                api_key="",

                model=""

            )

            try:

                engine.run_workflow(

                    workflow,

                    "Scheduled Execution"

                )

                executed += 1

            except Exception:

                pass

        return executed
