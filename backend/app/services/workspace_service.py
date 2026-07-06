
from app.config.database import db

from app.services.current_user_service import (
    CurrentUserService
)


class WorkspaceService:

    @staticmethod
    def create_workspace(
        name
    ):

        result = (
            db.client
            .table(
                "workspaces"
            )
            .insert(
                {
                    "name": name,
                    "owner_id":
                        CurrentUserService
                        .get_user_id()
                }
            )
            .execute()
        )

        workspace = result.data[0]

        db.client.table(
            "workspace_members"
        ).insert(
            {
                "workspace_id":
                    workspace["id"],

                "user_id":
                    CurrentUserService
                    .get_user_id(),

                "role":
                    "OWNER"
            }
        ).execute()

        return workspace

    @staticmethod
    def get_workspaces():

        user_id = (
            CurrentUserService
            .get_user_id()
        )

        memberships = (
            db.client
            .table(
                "workspace_members"
            )
            .select("*")
            .eq(
                "user_id",
                user_id
            )
            .execute()
        )

        workspace_ids = [

            m["workspace_id"]

            for m in memberships.data

        ]

        if not workspace_ids:

            return []

        result = (
            db.client
            .table(
                "workspaces"
            )
            .select("*")
            .in_(
                "id",
                workspace_ids
            )
            .execute()
        )

        return result.data
