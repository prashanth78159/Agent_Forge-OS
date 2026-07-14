
from app.config.database import db


class CurrentUserService:

    @staticmethod
    def get_user():

        try:

            response = db.client.auth.get_user()

            if response and response.user:

                return {
                    "id": response.user.id,
                    "email": response.user.email
                }

        except Exception:

            return None

        return None

    @staticmethod
    def get_user_id():

        user = CurrentUserService.get_user()

        if not user:
            return None

        return user["id"]
