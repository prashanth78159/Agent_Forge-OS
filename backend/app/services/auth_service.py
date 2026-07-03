
from app.config.database import db


class AuthService:

    @staticmethod
    def sign_up(
        email,
        password
    ):

        return (
            db.client.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )
        )

    @staticmethod
    def sign_in(
        email,
        password
    ):

        return (
            db.client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
        )

    @staticmethod
    def sign_out():

        return (
            db.client.auth.sign_out()
        )
