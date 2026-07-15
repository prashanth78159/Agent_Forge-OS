import streamlit as st
from app.services.current_user_service import CurrentUserService

class AdminGuard:
    @staticmethod
    def require_admin():
        user = CurrentUserService.get_user()
        if not user:
            st.error("Login required")
            st.stop()
        
        # Fetch role from database since session might be stale
        from app.config.database import db
        # Use .execute() and check length instead of .single() to avoid PGRST116 crashes
        res = db.client.table("user_profiles").select("role").eq("id", user["id"]).execute()

        if not res.data or res.data[0].get("role") != "Admin":
            st.error("Admin access required. No profile found or role mismatch.")
            st.stop()