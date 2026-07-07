
from app.config.database import db

from app.services.current_user_service import (
    CurrentUserService
)

from app.services.workflow_version_service import (
    WorkflowVersionService
)

from app.services.audit_service import (
    AuditService
)


class WorkflowService:

    @staticmethod
    def save_workflow(
        name,
        workflow_json
    ):

        existing = (
            db.client
            .table(
                "workflows"
            )
            .select("*")
            .eq(
                "name",
                name
            )
            .execute()
        )

        if existing.data:

            workflow = existing.data[0]

            db.client.table(
                "workflows"
            ).update(
                {
                    "workflow_json":
                        workflow_json
                }
            ).eq(
                "id",
                workflow["id"]
            ).execute()

            WorkflowVersionService.auto_create_version(

                str(
                    workflow["id"]
                ),

                workflow_json

            )

            AuditService.log_event(

                str(
                    workflow["id"]
                ),

                "UPDATE",

                f"Workflow {name} updated"

            )

            return workflow

        result = (
            db.client
            .table(
                "workflows"
            )
            .insert(
                {
                    "name": name,
                    "workflow_json": workflow_json,
                    "user_id":
                        CurrentUserService
                        .get_user_id()
                }
            )
            .execute()
        )

        workflow = result.data[0]

        WorkflowVersionService.create_version(

            workflow_id=
                str(workflow["id"]),

            version_number=1,

            workflow_json=
                workflow_json

        )

        AuditService.log_event(

            str(workflow["id"]),

            "CREATE",

            f"Workflow {name} created"

        )

        return result

    @staticmethod
    def get_workflows():

        user_id = (
            CurrentUserService
            .get_user_id()
        )

        result = (
            db.client
            .table(
                "workflows"
            )
            .select("*")
            .execute()
        )

        workflows = result.data

        if not user_id:

            return workflows

        return [

            workflow

            for workflow in workflows

            if (

                workflow.get(
                    "user_id"
                ) is None

                or

                str(
                    workflow.get(
                        "user_id"
                    )
                )

                ==

                str(user_id)

            )

        ]
