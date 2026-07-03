
from app.config.database import db


class WorkflowService:

    @staticmethod
    def save_workflow(
        name,
        workflow_json
    ):

        return (
            db.client
            .table("workflows")
            .insert(
                {
                    "name": name,
                    "workflow_json": workflow_json
                }
            )
            .execute()
        )

    @staticmethod
    def get_workflows():

        result = (
            db.client
            .table("workflows")
            .select("*")
            .execute()
        )

        return result.data
