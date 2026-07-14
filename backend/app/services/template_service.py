from app.config.database import db
from app.services.current_user_service import CurrentUserService


class TemplateService:

    @staticmethod
    def save_template(
        name,
        description,
        workflow_json
    ):
        user_id = CurrentUserService.get_user_id()
        return (
            db.client
            .table("workflow_templates")
            .insert(
                {
                    "name": name,
                    "description": description,
                    "workflow_json": workflow_json,
                    "user_id": user_id
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
