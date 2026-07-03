
from app.config.database import db


class UserService:

    @staticmethod
    def create_profile(
        user_id,
        email
    ):

        return (
            db.client
            .table(
                "user_profiles"
            )
            .upsert(
                {
                    "id": user_id,
                    "email": email
                }
            )
            .execute()
        )
