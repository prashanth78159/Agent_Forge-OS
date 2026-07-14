
from app.config.database import db

from app.services.base_data_service import BaseDataService


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
                        BaseDataService
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
                BaseDataService
                .get_user_id()
            )

            .execute()

        )

        return result.data
