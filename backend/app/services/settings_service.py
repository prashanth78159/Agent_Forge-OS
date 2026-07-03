
from app.config.database import db

class SettingsService:

    @staticmethod
    def save_setting(
        key,
        value
    ):

        return (
            db.client
            .table("user_settings")
            .upsert(
                {
                    "setting_key": key,
                    "setting_value": str(value)
                },
                on_conflict="setting_key"
            )
            .execute()
        )

    @staticmethod
    def get_setting(
        key
    ):

        result = (
            db.client
            .table("user_settings")
            .select("*")
            .eq(
                "setting_key",
                key
            )
            .execute()
        )

        if result.data:
            return result.data[0][
                "setting_value"
            ]

        return None
