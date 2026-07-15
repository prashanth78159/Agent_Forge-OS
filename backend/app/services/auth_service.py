from app.config.database import db
import streamlit as st
from typing import Optional, Dict

class AuthService:
    @staticmethod
    def login(email, password) -> Optional[Dict]:
        # Real credentials override for local testing/deployment
        if email == "plavishetti@gmail.com" and password == "Prashanth@12":
            res = db.client.table("user_profiles").select("*").eq("email", email).execute()
            if res.data:
                user_data = res.data[0]
                st.session_state.user = {
                    "id": user_data["id"],
                    "email": email,
                    "roles": [user_data.get("role", "Admin").lower()]
                }
                st.session_state.logged_in = True
                return st.session_state.user

        try:
            response = db.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if response.user:
                res = db.client.table("user_profiles").select("role").eq("id", response.user.id).execute()
                role = res.data[0].get("role", "Viewer") if res.data else "Viewer"
                st.session_state.user = {
                    "id": response.user.id,
                    "email": response.user.email,
                    "roles": [role.lower()]
                }
                st.session_state.logged_in = True
                return st.session_state.user
        except Exception:
            pass
        return None

    @staticmethod
    def sign_in(email, password) -> Optional[Dict]:
        """Alias for login to support existing UI calls"""
        return AuthService.login(email, password)

    @staticmethod
    def logout():
        db.client.auth.sign_out()
        st.session_state.clear()
        st.session_state.logged_in = False

    @staticmethod
    def get_current_user() -> Optional[Dict]:
        return st.session_state.get("user")

    @staticmethod
    def get_user_roles() -> list:
        user = AuthService.get_current_user()
        return user.get("roles", []) if user else []