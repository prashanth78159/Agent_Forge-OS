
from app.config.database import db

from app.services.current_user_service import (
    CurrentUserService
)


class RBACService:

    @staticmethod
    def get_role(
        workspace_id
    ):

        user_id = (
            CurrentUserService
            .get_user_id()
        )

        result = (
            db.client
            .table(
                "workspace_members"
            )
            .select("*")
            .eq(
                "workspace_id",
                workspace_id
            )
            .eq(
                "user_id",
                user_id
            )
            .execute()
        )

        if not result.data:

            return None

        return result.data[0]["role"]

    @staticmethod
    def can_edit(
        workspace_id
    ):

        role = (
            RBACService.get_role(
                workspace_id
            )
        )

        return role in [
            "OWNER",
            "ADMIN",
            "EDITOR"
        ]

    @staticmethod
    def can_manage_members(
        workspace_id
    ):

        role = (
            RBACService.get_role(
                workspace_id
            )
        )

        return role in [
            "OWNER",
            "ADMIN"
        ]

    @staticmethod
    def can_view(
        workspace_id
    ):

        role = (
            RBACService.get_role(
                workspace_id
            )
        )

        return role in [
            "OWNER",
            "ADMIN",
            "EDITOR",
            "VIEWER"
        ]
