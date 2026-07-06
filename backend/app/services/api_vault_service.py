
from app.config.database import db

from app.services.current_user_service import (
    CurrentUserService
)


class APIVaultService:

    @staticmethod
    def save_key(
        provider,
        api_key
    ):

        return (
            db.client
            .table(
                "user_api_keys"
            )
            .upsert(
                {
                    "user_id":
                        CurrentUserService
                        .get_user_id(),

                    "provider":
                        provider,

                    "api_key":
                        api_key
                }
            )
            .execute()
        )

    @staticmethod
    def get_keys():

        result = (

            db.client

            .table(
                "user_api_keys"
            )

            .select("*")

            .eq(
                "user_id",
                CurrentUserService
                .get_user_id()
            )

            .execute()

        )

        return result.data
