
import streamlit as st
from typing import List

class RBACService:
    @staticmethod
    def has_role(required_role: str) -> bool:
        user_roles = st.session_state.get("user", {}).get("roles", [])
        return required_role in user_roles

    @staticmethod
    def has_any_role(required_roles: List[str]) -> bool:
        user_roles = st.session_state.get("user", {}).get("roles", [])
        return any(role in user_roles for role in required_roles)

    @staticmethod
    def has_all_roles(required_roles: List[str]) -> bool:
        user_roles = st.session_state.get("user", {}).get("roles", [])
        return all(role in user_roles for role in required_roles)
