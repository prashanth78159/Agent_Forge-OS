
from app.config.database import db



class WorkspaceMemberService:

    @staticmethod
    def add_member(
        workspace_id,
        user_id,
        role="MEMBER"
    ):

        return (
            db.client
            .table(
                "workspace_members"
            )
            .insert(
                {
                    "workspace_id":
                        workspace_id,

                    "user_id":
                        user_id,

                    "role":
                        role
                }
            )
            .execute()
        )

    @staticmethod
    def get_members(
        workspace_id
    ):

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
            .execute()
        )

        return result.data
