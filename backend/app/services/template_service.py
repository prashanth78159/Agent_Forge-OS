
from app.config.database import db


class TemplateService:

    @staticmethod
    def save_template(
        name,
        description,
        workflow_json
    ):

        return (
            db.client
            .table("workflow_templates")
            .insert(
                {
                    "name": name,
                    "description": description,
                    "workflow_json": workflow_json
                }
            )
            .execute()
        )

    @staticmethod
    def get_templates():

        result = (
            db.client
            .table("workflow_templates")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data

    @staticmethod
    def get_template(
        template_id
    ):

        result = (
            db.client
            .table("workflow_templates")
            .select("*")
            .eq(
                "id",
                template_id
            )
            .execute()
        )

        if result.data:
            return result.data[0]

        return None
