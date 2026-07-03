
from app.config.database import db


class AnalyticsService:

    @staticmethod
    def get_metrics():

        workflows = (
            db.client
            .table("workflows")
            .select("*", count="exact")
            .execute()
        )

        templates = (
            db.client
            .table("workflow_templates")
            .select("*", count="exact")
            .execute()
        )

        executions = (
            db.client
            .table("executions")
            .select("*", count="exact")
            .execute()
        )

        workflow_runs = (
            db.client
            .table("workflow_executions")
            .select("*", count="exact")
            .execute()
        )

        return {

            "workflows":
                workflows.count or 0,

            "templates":
                templates.count or 0,

            "executions":
                executions.count or 0,

            "workflow_runs":
                workflow_runs.count or 0
        }
