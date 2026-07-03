
import uuid

from app.services.llm_service import LLMService
from app.services.workflow_execution_service import (
    WorkflowExecutionService
)
from app.services.workflow_status_service import (
    WorkflowStatusService
)
from app.config.database import db


class ExecutionEngine:

    def __init__(
        self,
        provider,
        api_key,
        model
    ):

        self.llm = LLMService(
            provider,
            api_key,
            model
        )

    def execute_node(
        self,
        execution_id,
        node
    ):

        node_id = node.get(
            "id",
            "node"
        )

        prompt = node.get(
            "prompt",
            f"Execute node {node_id}"
        )

        WorkflowStatusService.set_node_status(
            execution_id,
            node_id,
            "RUNNING"
        )

        (
            output,
            prompt_tokens,
            completion_tokens,
            total_cost
        ) = self.llm.generate(
            prompt
        )

        WorkflowExecutionService.save_output(
            execution_id,
            node_id,
            output
        )

        WorkflowStatusService.set_node_status(
            execution_id,
            node_id,
            "COMPLETED"
        )

        return output

    def run_workflow(
        self,
        workflow,
        task
    ):

        execution_id = str(
            uuid.uuid4()
        )

        WorkflowExecutionService.save_execution(
            execution_id,
            str(
                workflow.get(
                    "id",
                    "workflow"
                )
            ),
            "RUNNING"
        )

        nodes = workflow.get(
            "workflow_json",
            {}
        ).get(
            "nodes",
            []
        )

        outputs = {}

        total = max(
            len(nodes),
            1
        )

        for index, node in enumerate(nodes):

            context = "\n\n".join(
                str(v)
                for v in outputs.values()
            )

            if context:

                node["prompt"] = (
                    "Previous Workflow Context:\n\n"
                    + context
                    + "\n\nCurrent Instruction:\n\n"
                    + node.get(
                        "prompt",
                        task
                    )
                )

            else:

                node["prompt"] = node.get(
                    "prompt",
                    task
                )

            outputs[
                node["id"]
            ] = self.execute_node(
                execution_id,
                node
            )

            WorkflowStatusService.update_progress(
                execution_id,
                int(
                    ((index + 1) / total)
                    * 100
                )
            )

        db.client.table(
            "workflow_executions"
        ).update(
            {
                "status": "COMPLETED"
            }
        ).eq(
            "id",
            execution_id
        ).execute()

        return {

            "execution_id":
                execution_id,

            "node_outputs":
                outputs,

            "final":
                list(
                    outputs.values()
                )[-1]
                if outputs
                else ""

        }
