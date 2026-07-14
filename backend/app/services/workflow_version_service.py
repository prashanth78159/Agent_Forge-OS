from app.config.database import db
from app.services.base_data_service import BaseDataService


class WorkflowVersionService:

    @staticmethod
    def get_next_version(
        workflow_id
    ):

        result = (
            db.client
            .table(
                "workflow_versions"
            )
            .select("* ")
            .eq(
                "workflow_id",
                workflow_id
            )
            .order(
                "version_number",
                desc=True
            )
            .limit(1)
            .execute()
        )

        if not result.data:

            return 1

        return (
            result.data[0]
            ["version_number"]
            + 1
        )

    @staticmethod
    def create_version(
        workflow_id,
        version_number,
        workflow_json
    ):
        user_id = BaseDataService.get_user_id()

        return (
            db.client
            .table(
                "workflow_versions"
            )
            .insert(
                {
                    "workflow_id":
                        workflow_id,

                    "version_number":
                        version_number,

                    "workflow_json":
                        workflow_json,

                    "user_id":
                        user_id
                }
            )
            .execute()
        )

    @staticmethod
    def auto_create_version(
        workflow_id,
        workflow_json
    ):

        version = (
            WorkflowVersionService
            .get_next_version(
                workflow_id
            )
        )

        return (
            WorkflowVersionService
            .create_version(
                workflow_id,
                version,
                workflow_json
            )
        )

    @staticmethod
    def get_versions(
        workflow_id
    ):

        result = (
            db.client
            .table(
                "workflow_versions"
            )
            .select("* ")
            .eq(
                "workflow_id",
                workflow_id
            )
            .order(
                "version_number",
                desc=True
            )
            .execute()
        )

        return result.data
