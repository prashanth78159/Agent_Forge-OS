from app.config.database import db
import streamlit as st
from typing import Optional, Dict

class AuthService:
    @staticmethod
    def sign_in(email, password) -> Optional[Dict]:
        try:
            response = db.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if response.user:
                # Fetch user roles from user_metadata or a separate table if available
                # For now, we'll assign roles based on the provided mock logic or a default
                # In a real app, you'd fetch this from your Supabase user metadata or a roles table
                if email == "admin@example.com":
                    roles = ["admin", "manager", "director", "finance"]
                elif email == "manager@example.com":
                    roles = ["manager"]
                elif email == "director@example.com":
                    roles = ["director"]
                elif email == "finance@example.com":
                    roles = ["finance"]
                else:
                    roles = ["user"] # Default role

                st.session_state.user = {
                    "id": response.user.id,
                    "email": response.user.email,
                    "roles": roles
                }
                return st.session_state.user
            return None
        except Exception as e:
            st.error(f"Authentication failed: {e}")
            return None

    @staticmethod
    def login(email, password) -> Optional[Dict]:
        # Refactor login to use the new sign_in method
        return AuthService.sign_in(email, password)

    @staticmethod
    def logout():
        try:
            db.client.auth.sign_out()
            if "user" in st.session_state:
                del st.session_state.user
            st.session_state.logged_in = False
        except Exception as e:
            st.error(f"Logout failed: {e}")

    @staticmethod
    def get_current_user() -> Optional[Dict]:
        return st.session_state.get("user")

    @staticmethod
    def get_user_roles() -> list:
        user = AuthService.get_current_user()
        return user.get("roles", []) if user else []
