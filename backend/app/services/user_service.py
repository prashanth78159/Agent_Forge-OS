from app.config.database import db
from app.services.base_data_service import BaseDataService

class UserService:
    @staticmethod
    def get_all_users():
        # In Supabase, auth.users is protected. We typically mirror users to a public.profiles table
        # for easier management, or use the admin API. For this enterprise logic,
        # we assume a 'profiles' table exists that mirrors the auth users.
        result = db.client.table("profiles").select("*").execute()
        return result.data

    @staticmethod
    def create_user(email, password, roles=None):
        # Note: In a production environment, this would use the Supabase Admin Auth API
        # which requires a service_role key.
        response = db.client.auth.admin.create_user({
            "email": email,
            "password": password,
            "user_metadata": {"roles": roles or ["user"]},
            "email_confirm": True
        })
        return response

    @staticmethod
    def update_user_status(user_id, disabled=False):
        # Updating user metadata to track disabled state
        response = db.client.auth.admin.update_user_by_id(
            user_id,
            {"user_metadata": {"disabled": disabled}}
        )
        return response