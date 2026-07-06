
import uuid

from app.config.database import db

from app.services.llm_service import (
    LLMService
)

from app.services.workflow_execution_service import (
    WorkflowExecutionService
)

from app.services.workflow_status_service import (
    WorkflowStatusService
)

from app.services.workflow_metrics_service import (
    WorkflowMetricsService
)

from app.services.error_service import (
    ErrorService
)

from app.core.runtime.dag_executor import (
    DAGExecutor
)
from app.services.execution_state_service import (
    ExecutionStateService
)


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
        node,
        context=""
    ):

        from app.services.approval_service import (
            ApprovalService
        )

        node_id = node.get(
            "id",
            "node"
        )

        if ApprovalService.is_approval_node(
            node
        ):

            ApprovalService.create_request(
                execution_id,
                node_id
            )

            ExecutionStateService.save_state(

                execution_id,

                node_id,

                "WAITING_APPROVAL"

            )

            return {
                "execution_id": execution_id,
                "status": "WAITING_APPROVAL"
            }

        base_prompt = node.get(
            "prompt",
            f"Execute node {node_id}"
        )

        if context:

            prompt = (
                "Dependency Context:\n\n"
                + context
                + "\n\nTask:\n\n"
                + base_prompt
            )

        else:

            prompt = base_prompt

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

        return {

            "output":
                output,

            "prompt_tokens":
                prompt_tokens,

            "completion_tokens":
                completion_tokens,

            "cost":
                total_cost

        }


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

        from app.services.audit_service import (
            AuditService
        )

        AuditService.log_event(

            str(
                workflow.get(
                    "id",
                    "workflow"
                )
            ),

            "EXECUTE",

            "Workflow executed"

        )

        workflow_json = workflow.get(
            "workflow_json",
            {}
        )

        nodes = workflow_json.get(
            "nodes",
            []
        )

        edges = workflow_json.get(
            "edges",
            []
        )

        dag = DAGExecutor(
            nodes,
            edges
        )

        outputs = {}

        completed = set()

        total_nodes = max(
            len(nodes),
            1
        )

        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_cost = 0

        while len(completed) < len(nodes):

            ready_nodes = dag.get_ready_nodes(
                completed
            )

            progress_made = False

            for node in ready_nodes:

                node_id = node["id"]

                if node_id in completed:

                    continue

                deps = dag.get_dependencies(
                    node_id
                )

                context = "\n\n".join(

                    outputs[dep]

                    for dep in deps

                    if dep in outputs

                )

                if (
                    not deps
                    and
                    not node.get("prompt")
                ):

                    node["prompt"] = task

                retry_count = node.get(
                    "retries",
                    3
                )

                last_error = None

                for attempt in range(
                    retry_count + 1
                ):

                    try:

                        result = self.execute_node(
                            execution_id,
                            node,
                            context
                        )

                        last_error = None

                        break

                  

                    except Exception as e:

                        if str(e) == "WAITING_APPROVAL":

                            raise e

                        last_error = e

                        WorkflowStatusService.set_node_status(
                            execution_id,
                            node_id,
                            "FAILED"
                        )

                if last_error:

                    if str(last_error) == "WAITING_APPROVAL":

                        return {

                            "execution_id":
                                execution_id,

                            "status":
                                "WAITING_APPROVAL"

                        }

                    ErrorService.log_error(

                        execution_id,

                        node_id,

                        str(last_error)

                    )

                    raise last_error

                outputs[node_id] = (
                    result["output"]
                )

                total_prompt_tokens += (
                    result["prompt_tokens"]
                )

                total_completion_tokens += (
                    result["completion_tokens"]
                )

                total_cost += (
                    result["cost"]
                )

                completed.add(
                    node_id
                )

                WorkflowStatusService.update_progress(
                    execution_id,
                    int(
                        (
                            len(completed)
                            /
                            total_nodes
                        ) * 100
                    )
                )

                progress_made = True

            if not progress_made:

                raise Exception(
                    "Workflow contains circular dependencies."
                )

        WorkflowMetricsService.save_metrics(

            execution_id,

            total_nodes,

            len(completed),

            total_prompt_tokens,

            total_completion_tokens,

            total_cost

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

        return {

            "execution_id":
                execution_id,

            "node_outputs":
                outputs,

            "prompt_tokens":
                total_prompt_tokens,

            "completion_tokens":
                total_completion_tokens,

            "cost":
                total_cost,

            "final":
                list(
                    outputs.values()
                )[-1]
                if outputs
                else ""

        }
