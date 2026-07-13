
import streamlit as st
from typing import Optional, Dict

class AuthService:
    @staticmethod
    def login(email, password) -> Optional[Dict]:
        if email == "admin@example.com" and password == "adminpass":
            st.session_state.user = {"id": "admin_id", "email": "admin@example.com", "roles": ["admin", "manager", "director", "finance"]}
            return st.session_state.user
        elif email == "manager@example.com" and password == "managerpass":
            st.session_state.user = {"id": "manager_id", "email": "manager@example.com", "roles": ["manager"]}
            return st.session_state.user
        elif email == "director@example.com" and password == "directorpass":
            st.session_state.user = {"id": "director_id", "email": "director@example.com", "roles": ["director"]}
            return st.session_state.user
        elif email == "finance@example.com" and password == "financepass":
            st.session_state.user = {"id": "finance_id", "email": "finance@example.com", "roles": ["finance"]}
            return st.session_state.user
        else:
            return None

    @staticmethod
    def logout():
        if "user" in st.session_state:
            del st.session_state.user
        st.session_state.logged_in = False

    @staticmethod
    def get_current_user() -> Optional[Dict]:
        return st.session_state.get("user")

    @staticmethod
    def get_user_roles() -> list:
        user = AuthService.get_current_user()
        return user.get("roles", []) if user else []
